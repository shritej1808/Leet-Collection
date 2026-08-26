#!/usr/bin/env python3
"""
generate_readme.py
-------------------
Scans a LeetSync-synced repo (folders named like "189-rotate-array"),
pulls problem metadata (difficulty, topics, title) from LeetCode's public
GraphQL API, figures out which language each solution is written in,
and writes a fully auto-updating README.md with:

  - Badges (total solved, per-difficulty counts)
  - A live LeetCode stats card
  - A quickchart.io difficulty pie chart + topic bar chart
    (rendered live by GitHub's markdown viewer, no image files needed)
  - A sortable-looking table of every problem solved
  - A "last updated" timestamp

Designed to be run by a GitHub Action on every push, since LeetSync
commits directly to this repo whenever you solve something new.

Usage:
    python scripts/generate_readme.py

Env vars (all optional):
    LEETCODE_USERNAME   - your LeetCode username, for the live stats card
    GITHUB_REPOSITORY   - "owner/repo", auto-set inside GitHub Actions
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE_FILE = REPO_ROOT / ".leet-meta-cache.json"
FOLDER_RE = re.compile(r"^(\d+)-([a-z0-9-]+)$")

LANG_BY_EXT = {
    ".py": "Python",
    ".java": "Java",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".cpp": "C++",
    ".cc": "C++",
    ".c": "C",
    ".cs": "C#",
    ".go": "Go",
    ".rb": "Ruby",
    ".rs": "Rust",
    ".kt": "Kotlin",
    ".swift": "Swift",
}

DIFFICULTY_COLOR = {
    "Easy": "3CB371",
    "Medium": "FFA116",
    "Hard": "FF4C4C",
    "Unknown": "999999",
}

DIFFICULTY_EMOJI = {
    "Easy": "🟢",
    "Medium": "🟡",
    "Hard": "🔴",
    "Unknown": "⚪",
}

GRAPHQL_QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionFrontendId
    title
    difficulty
    topicTags { name }
  }
}
"""


def load_cache():
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_cache(cache):
    CACHE_FILE.write_text(json.dumps(cache, indent=2, sort_keys=True), encoding="utf-8")


def _fetch_from_official_graphql(slug):
    payload = json.dumps(
        {"query": GRAPHQL_QUERY, "variables": {"titleSlug": slug}}
    ).encode()
    req = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "https://leetcode.com",
            "Referer": f"https://leetcode.com/problems/{slug}/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        },
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    q = data["data"]["question"]
    return {
        "title": q["title"],
        "difficulty": q["difficulty"],
        "topics": [t["name"] for t in q["topicTags"]],
    }


def _fetch_from_alfa_mirror(slug):
    # Public community mirror of LeetCode's question data. Used as a
    # fallback since leetcode.com sometimes blocks non-browser clients
    # (e.g. Cloudflare bot checks on hosted CI runners).
    url = f"https://alfa-leetcode-api.onrender.com/select?titleSlug={slug}"
    req = urllib.request.Request(url, headers={"User-Agent": "leet-collection-readme-bot"})
    with urllib.request.urlopen(req, timeout=12) as resp:
        data = json.loads(resp.read())
    return {
        "title": data.get("questionTitle") or slug.replace("-", " ").title(),
        "difficulty": data.get("difficulty", "Unknown"),
        "topics": [t.get("name", t) if isinstance(t, dict) else t
                   for t in data.get("topicTags", [])],
    }


def fetch_question_meta(slug, cache):
    """Fetch difficulty/title/topics for a problem slug, with local caching
    so we don't hit external APIs for problems we've already resolved."""
    if slug in cache:
        return cache[slug]

    meta = None
    for fetcher in (_fetch_from_official_graphql, _fetch_from_alfa_mirror):
        try:
            meta = fetcher(slug)
            break
        except Exception as e:  # network hiccup, rate limit, blocked, etc.
            print(f"  [warn] {fetcher.__name__} failed for {slug}: {e}", file=sys.stderr)

    if meta is None:
        meta = {
            "title": slug.replace("-", " ").title(),
            "difficulty": "Unknown",
            "topics": [],
        }

    cache[slug] = meta
    time.sleep(0.4)  # be polite to the APIs
    return meta


def detect_language(folder: Path):
    langs = set()
    for f in folder.iterdir():
        if f.suffix in LANG_BY_EXT:
            langs.add(LANG_BY_EXT[f.suffix])
    return ", ".join(sorted(langs)) if langs else "—"


def solution_file(folder: Path):
    for f in folder.iterdir():
        if f.suffix in LANG_BY_EXT:
            return f.name
    return None


def date_added(folder: Path):
    """First commit date that touched this folder, so the table can show
    when each problem was solved."""
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%aI", "--follow", "--",
             str(folder)],
            cwd=REPO_ROOT, capture_output=True, text=True, timeout=10,
        )
        lines = [l for l in out.stdout.strip().splitlines() if l]
        if lines:
            return lines[-1][:10]
    except Exception:
        pass
    return "—"


def collect_problems():
    cache = load_cache()
    problems = []
    for entry in sorted(REPO_ROOT.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        m = FOLDER_RE.match(entry.name)
        if not m:
            continue
        number, slug = m.groups()
        meta = fetch_question_meta(slug, cache)
        problems.append({
            "number": int(number),
            "slug": slug,
            "folder": entry.name,
            "title": meta["title"],
            "difficulty": meta["difficulty"],
            "topics": meta["topics"],
            "language": detect_language(entry),
            "solution_file": solution_file(entry),
            "date": date_added(entry),
        })
    save_cache(cache)
    problems.sort(key=lambda p: p["number"])
    return problems


def quickchart_pie_url(counts):
    config = {
        "type": "doughnut",
        "data": {
            "labels": list(counts.keys()),
            "datasets": [{
                "data": list(counts.values()),
                "backgroundColor": [f"#{DIFFICULTY_COLOR.get(k, '999999')}" for k in counts],
            }],
        },
        "options": {
            "plugins": {
                "legend": {"labels": {"color": "gray", "font": {"size": 14}}},
                "title": {"display": True, "text": "Solved by Difficulty", "color": "gray"},
            }
        },
    }
    qs = urllib.parse.quote(json.dumps(config))
    return f"https://quickchart.io/chart?c={qs}&backgroundColor=transparent&width=380&height=260"


def quickchart_topics_url(topic_counts, top_n=8):
    top = sorted(topic_counts.items(), key=lambda kv: -kv[1])[:top_n]
    if not top:
        return None
    config = {
        "type": "bar",
        "data": {
            "labels": [t for t, _ in top],
            "datasets": [{"label": "Problems", "data": [c for _, c in top],
                          "backgroundColor": "#5865F2"}],
        },
        "options": {
            "indexAxis": "y",
            "plugins": {"legend": {"display": False},
                        "title": {"display": True, "text": "Top Topics", "color": "gray"}},
            "scales": {"x": {"ticks": {"color": "gray"}}, "y": {"ticks": {"color": "gray"}}},
        },
    }
    qs = urllib.parse.quote(json.dumps(config))
    return f"https://quickchart.io/chart?c={qs}&backgroundColor=transparent&width=420&height=280"


def badge(label, message, color):
    l = urllib.parse.quote(label)
    m = urllib.parse.quote(str(message))
    return f"https://img.shields.io/badge/{l}-{m}-{color}?style=for-the-badge"


def build_readme(problems):
    repo = os.environ.get("GITHUB_REPOSITORY", "shritej1808/Leet-Collection")
    username = os.environ.get("LEETCODE_USERNAME", "").strip()

    total = len(problems)
    diff_counts = {"Easy": 0, "Medium": 0, "Hard": 0}
    topic_counts = {}
    for p in problems:
        if p["difficulty"] in diff_counts:
            diff_counts[p["difficulty"]] += 1
        for t in p["topics"]:
            topic_counts[t] = topic_counts.get(t, 0) + 1

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = []
    lines.append(
        "<h1 align=\"center\">🧠 Leet-Collection</h1>\n"
        "<p align=\"center\">Auto-generated LeetCode solution archive, "
        "synced with <a href=\"https://github.com/3ba2ii/LeetSync\">LeetSync</a> "
        "and self-updating on every push.</p>\n"
    )

    lines.append('<p align="center">')
    lines.append(f'  <img src="{badge("Solved", total, "5865F2")}" alt="total solved" />')
    lines.append(f'  <img src="{badge("Easy", diff_counts["Easy"], DIFFICULTY_COLOR["Easy"])}" />')
    lines.append(f'  <img src="{badge("Medium", diff_counts["Medium"], DIFFICULTY_COLOR["Medium"])}" />')
    lines.append(f'  <img src="{badge("Hard", diff_counts["Hard"], DIFFICULTY_COLOR["Hard"])}" />')
    lines.append(f'  <img src="{badge("Last Updated", now.replace(" ", "."), "444")}" />')
    lines.append("</p>\n")

    if username:
        lines.append(
            f'<p align="center">\n'
            f'  <img src="https://leetcard.jacoblin.cool/{username}?theme=dark&ext=heatmap" '
            f'alt="LeetCode stats for {username}" />\n'
            f"</p>\n"
        )
    else:
        lines.append(
            "> ℹ️ Set the `LEETCODE_USERNAME` repo variable to show a live "
            "LeetCode stats card + submission heatmap here.\n"
        )

    lines.append("## 📊 Breakdown\n")
    lines.append('<p align="center">')
    lines.append(f'  <img src="{quickchart_pie_url(diff_counts)}" alt="difficulty breakdown" width="380"/>')
    topics_url = quickchart_topics_url(topic_counts)
    if topics_url:
        lines.append(f'  <img src="{topics_url}" alt="top topics" width="420"/>')
    lines.append("</p>\n")

    lines.append("## 📚 Solutions\n")
    lines.append("| # | Problem | Difficulty | Language | Topics | Solved |")
    lines.append("|---|---------|:----------:|----------|--------|:------:|")
    for p in problems:
        emoji = DIFFICULTY_EMOJI.get(p["difficulty"], "⚪")
        leet_url = f"https://leetcode.com/problems/{p['slug']}/"
        title_cell = f"[{p['title']}]({leet_url})"
        topics_cell = ", ".join(p["topics"][:3]) + ("…" if len(p["topics"]) > 3 else "")
        folder_link = f"[{p['folder']}](./{p['folder']})"
        lines.append(
            f"| {p['number']} | {title_cell} <br/> {folder_link} | "
            f"{emoji} {p['difficulty']} | {p['language']} | {topics_cell or '—'} | {p['date']} |"
        )

    lines.append(
        f"\n---\n<p align=\"center\"><sub>Auto-generated on {now} by "
        f"<code>scripts/generate_readme.py</code> · "
        f"<a href=\"https://github.com/{repo}/actions\">view workflow runs</a></sub></p>\n"
    )

    return "\n".join(lines)


def main():
    problems = collect_problems()
    readme = build_readme(problems)
    (REPO_ROOT / "README.md").write_text(readme, encoding="utf-8")
    print(f"Wrote README.md with {len(problems)} problems.")


if __name__ == "__main__":
    main()
