#!/usr/bin/env python3
"""
Commit Roast — pipes every solution file changed in a push through an LLM,
in the voice of a strict, unimpressed technical interviewer, and posts the
result as a GitHub commit comment.

Uses Groq's free inference API (no credit card required) via Groq's own SDK.

Env vars (all set by the workflow):
  GROQ_API_KEY        required. Free key from console.groq.com.
  GITHUB_TOKEN        required. Used to post the commit comment.
  GITHUB_REPOSITORY   "owner/repo", provided by GitHub Actions.
  BEFORE_SHA          github.event.before
  AFTER_SHA           github.event.after (the commit we comment on)
  ROAST_MODEL         optional, defaults to a fast/free Groq model.
"""

import os
import re
import subprocess
import sys

import requests
from groq import Groq

MAX_FILES_PER_PUSH = 5
MAX_CHARS_PER_FILE = 6000  # keep prompts cheap; solutions are short anyway
SOLUTION_EXTENSIONS = {".java", ".py", ".js", ".ts", ".cpp", ".c", ".go", ".rs", ".kt"}
IGNORED_PREFIXES = ("scripts/", ".github/", "docs/")

SYSTEM_PROMPT = """You are a strict, unimpressed senior technical interviewer \
reviewing a candidate's code live. You have seen ten thousand solutions to \
this exact class of problem and are hard to impress. Write exactly ONE \
sentence (under 200 characters) reacting to the code you're given: call out \
naming, complexity, edge cases, or style if there's something to call out. \
If the code is genuinely clean, grudgingly admit it in the same dry, \
unimpressed tone — do not invent flaws that aren't there. Never be cruel or \
personal, stay professional-savage, like a tough but fair interview panel. \
Output ONLY the sentence. No preamble, no quotes, no markdown."""


def sh(*args):
    return subprocess.run(args, capture_output=True, text=True, check=True).stdout.strip()


def changed_files(before_sha, after_sha):
    """List files added/modified in this push."""
    if not before_sha or set(before_sha) == {"0"}:
        # First push of a new branch — no meaningful 'before'. Diff against
        # the parent of the pushed commit instead, falling back to the
        # commit's own tree if it has no parent (first commit ever).
        try:
            before_sha = sh("git", "rev-parse", f"{after_sha}^")
        except subprocess.CalledProcessError:
            out = sh("git", "show", "--pretty=", "--name-status", after_sha)
            return _parse_name_status(out)
    out = sh("git", "diff", "--name-status", before_sha, after_sha)
    return _parse_name_status(out)


def _parse_name_status(out):
    files = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status, path = parts[0], parts[-1]
        if status.startswith("D"):  # skip deletions
            continue
        files.append(path)
    return files


def is_solution_file(path):
    if path.startswith(IGNORED_PREFIXES):
        return False
    _, ext = os.path.splitext(path)
    return ext in SOLUTION_EXTENSIONS


def guess_problem_label(path):
    """'189-rotate-array/rotate-array.java' -> '#189 rotate array'"""
    folder = path.split("/")[0]
    m = re.match(r"(\d+)-(.+)", folder)
    if m:
        return f"#{m.group(1)} {m.group(2).replace('-', ' ')}"
    return path


def roast(client, model, path):
    try:
        with open(path, "r", errors="replace") as f:
            code = f.read()[:MAX_CHARS_PER_FILE]
    except OSError:
        return None
    if not code.strip():
        return None

    label = guess_problem_label(path)
    user_msg = f"Problem: {label}\nFile: {path}\n\n```\n{code}\n```"

    resp = client.chat.completions.create(
        model=model,
        max_completion_tokens=400,
        # openai/gpt-oss-* models on Groq are reasoning models: they spend
        # part of the token budget "thinking" before writing the answer.
        # Keep that spend small and hide it from the final content so we
        # don't burn the whole budget on reasoning and get an empty reply.
        reasoning_effort="low",
        reasoning_format="hidden",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
    )
    text = (resp.choices[0].message.content or "").strip()
    if not text:
        return None
    return label, text


def post_commit_comment(repo, sha, token, body):
    url = f"https://api.github.com/repos/{repo}/commits/{sha}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    r = requests.post(url, headers=headers, json={"body": body}, timeout=30)
    r.raise_for_status()


def main():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("GROQ_API_KEY not set — skipping roast (add it as a repo secret).")
        return

    repo = os.environ["GITHUB_REPOSITORY"]
    token = os.environ["GITHUB_TOKEN"]
    before_sha = os.environ.get("BEFORE_SHA", "")
    after_sha = os.environ["AFTER_SHA"]
    model = os.environ.get("ROAST_MODEL", "openai/gpt-oss-120b")

    files = [f for f in changed_files(before_sha, after_sha) if is_solution_file(f)]
    if not files:
        print("No solution files changed in this push — nothing to roast.")
        return
    files = files[:MAX_FILES_PER_PUSH]

    client = Groq(api_key=api_key)
    results = []
    for path in files:
        result = roast(client, model, path)
        if result:
            results.append(result)

    if not results:
        print("Nothing worth roasting.")
        return

    lines = ["**🎤 Commit Roast — the interviewer has notes:**", ""]
    for label, line in results:
        lines.append(f"- **{label}** — {line}")
    body = "\n".join(lines)

    post_commit_comment(repo, after_sha, token, body)
    print("Posted roast:\n" + body)


if __name__ == "__main__":
    sys.exit(main())
