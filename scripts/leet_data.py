#!/usr/bin/env python3
"""
leet_data.py
------------
Shared core for the Leet-Collection automation: scans the repo for
LeetSync-created problem folders, resolves each problem's metadata
(difficulty/topics/title) from LeetCode's public API, detects the
solution language, figures out solve dates from git history, and
computes an achievements/trophy list.

Both generate_readme.py and generate_site.py import from here so the
README and the live site are always built from exactly the same data.
"""

import json
import re
import subprocess
import sys
import time
import urllib.request
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE_FILE = REPO_ROOT / ".leet-meta-cache.json"
FOLDER_RE = re.compile(r"^(\d+)-([a-z0-9-]+)$")

LANG_BY_EXT = {
    ".py": "Python", ".java": "Java", ".js": "JavaScript", ".ts": "TypeScript",
    ".cpp": "C++", ".cc": "C++", ".c": "C", ".cs": "C#", ".go": "Go",
    ".rb": "Ruby", ".rs": "Rust", ".kt": "Kotlin", ".swift": "Swift",
}

DIFFICULTY_COLOR = {"Easy": "3CB371", "Medium": "FFA116", "Hard": "FF4C4C", "Unknown": "999999"}
DIFFICULTY_EMOJI = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴", "Unknown": "⚪"}

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


# ---------------------------------------------------------------- metadata --

def load_cache():
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_cache(cache):
    CACHE_FILE.write_text(json.dumps(cache, indent=2, sort_keys=True))


def _fetch_from_official_graphql(slug):
    payload = json.dumps({"query": GRAPHQL_QUERY, "variables": {"titleSlug": slug}}).encode()
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
    return {"title": q["title"], "difficulty": q["difficulty"],
            "topics": [t["name"] for t in q["topicTags"]]}


def _fetch_from_alfa_mirror(slug):
    # Community mirror of LeetCode's question data — fallback for when
    # leetcode.com itself blocks non-browser clients on hosted CI runners.
    url = f"https://alfa-leetcode-api.onrender.com/select?titleSlug={slug}"
    req = urllib.request.Request(url, headers={"User-Agent": "leet-collection-bot"})
    with urllib.request.urlopen(req, timeout=12) as resp:
        data = json.loads(resp.read())
    return {
        "title": data.get("questionTitle") or slug.replace("-", " ").title(),
        "difficulty": data.get("difficulty", "Unknown"),
        "topics": [t.get("name", t) if isinstance(t, dict) else t
                   for t in data.get("topicTags", [])],
    }


def fetch_question_meta(slug, cache):
    if slug in cache:
        return cache[slug]
    meta = None
    for fetcher in (_fetch_from_official_graphql, _fetch_from_alfa_mirror):
        try:
            meta = fetcher(slug)
            break
        except Exception as e:
            print(f"  [warn] {fetcher.__name__} failed for {slug}: {e}", file=sys.stderr)
    if meta is None:
        meta = {"title": slug.replace("-", " ").title(), "difficulty": "Unknown", "topics": []}
    cache[slug] = meta
    time.sleep(0.4)
    return meta


# ------------------------------------------------------------- filesystem --

def detect_language(folder: Path):
    langs = set()
    for f in folder.iterdir():
        if f.suffix in LANG_BY_EXT:
            langs.add(LANG_BY_EXT[f.suffix])
    return sorted(langs)


def solution_file(folder: Path):
    for f in folder.iterdir():
        if f.suffix in LANG_BY_EXT:
            return f.name
    return None


def date_added(folder: Path):
    """First commit date that added this folder (solve date, effectively)."""
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%aI", "--follow", "--", str(folder)],
            cwd=REPO_ROOT, capture_output=True, text=True, timeout=10,
        )
        lines = [l for l in out.stdout.strip().splitlines() if l]
        if lines:
            return lines[-1][:10]
    except Exception:
        pass
    return None


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
        langs = detect_language(entry)
        problems.append({
            "number": int(number),
            "slug": slug,
            "folder": entry.name,
            "title": meta["title"],
            "difficulty": meta["difficulty"],
            "topics": meta["topics"],
            "languages": langs,
            "language": ", ".join(langs) if langs else "—",
            "solution_file": solution_file(entry),
            "date": date_added(entry),
        })
    save_cache(cache)
    problems.sort(key=lambda p: p["number"])
    return problems


# ------------------------------------------------------------ achievements --

ACHIEVEMENTS = [
    {"id": "first-blood", "name": "First Blood", "icon": "🩸",
     "desc": "Solve your first problem",
     "rule": lambda p, s: len(p) >= 1},
    {"id": "getting-warm", "name": "Getting Warmed Up", "icon": "🔥",
     "desc": "Solve 5 problems",
     "rule": lambda p, s: len(p) >= 5},
    {"id": "quarter-century", "name": "Quarter Century", "icon": "🥉",
     "desc": "Solve 25 problems",
     "rule": lambda p, s: len(p) >= 25},
    {"id": "half-century", "name": "Half Century", "icon": "🥈",
     "desc": "Solve 50 problems",
     "rule": lambda p, s: len(p) >= 50},
    {"id": "century-club", "name": "Century Club", "icon": "🥇",
     "desc": "Solve 100 problems",
     "rule": lambda p, s: len(p) >= 100},
    {"id": "easy-rider", "name": "Easy Rider", "icon": "🟢",
     "desc": "Solve 10 Easy problems",
     "rule": lambda p, s: s["diff"]["Easy"] >= 10},
    {"id": "middle-manager", "name": "Middle Manager", "icon": "🟡",
     "desc": "Solve 10 Medium problems",
     "rule": lambda p, s: s["diff"]["Medium"] >= 10},
    {"id": "hard-mode", "name": "Hard Mode", "icon": "🔴",
     "desc": "Solve your first Hard problem",
     "rule": lambda p, s: s["diff"]["Hard"] >= 1},
    {"id": "hardcore", "name": "Hardcore", "icon": "💀",
     "desc": "Solve 10 Hard problems",
     "rule": lambda p, s: s["diff"]["Hard"] >= 10},
    {"id": "well-rounded", "name": "Well Rounded", "icon": "🧭",
     "desc": "Solve problems across 5+ different topics",
     "rule": lambda p, s: len(s["topics"]) >= 5},
    {"id": "polyglot", "name": "Polyglot", "icon": "🌐",
     "desc": "Solve problems in 3+ languages",
     "rule": lambda p, s: len(s["languages"]) >= 3},
    {"id": "speed-demon", "name": "Speed Demon", "icon": "⚡",
     "desc": "Solve 3+ problems in a single day",
     "rule": lambda p, s: s["max_per_day"] >= 3},
    {"id": "consistency-king", "name": "Consistency King", "icon": "📆",
     "desc": "Solve on 7+ different days",
     "rule": lambda p, s: len(s["days"]) >= 7},
]


def _achievement_stats(problems):
    diff = defaultdict(int)
    topics = set()
    languages = set()
    days = defaultdict(int)
    for p in problems:
        diff[p["difficulty"]] += 1
        topics.update(p["topics"])
        languages.update(p["languages"])
        if p["date"]:
            days[p["date"]] += 1
    return {
        "diff": diff,
        "topics": topics,
        "languages": languages,
        "days": days,
        "max_per_day": max(days.values()) if days else 0,
    }


def compute_achievements(problems):
    stats = _achievement_stats(problems)
    out = []
    for a in ACHIEVEMENTS:
        unlocked = bool(a["rule"](problems, stats))
        out.append({"id": a["id"], "name": a["name"], "icon": a["icon"],
                    "desc": a["desc"], "unlocked": unlocked})
    return out
