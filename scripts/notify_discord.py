#!/usr/bin/env python3
"""
notify_discord.py
------------------
Optional: if a DISCORD_WEBHOOK_URL env var / secret is set, this posts
a rich embed to Discord announcing any problems solved since the last
run. Keeps its own small state file (.leet-notified.json) so it never
announces the same solve twice, even across re-runs.

Safe to always include in the workflow — it silently no-ops if the
webhook secret isn't configured.
"""

import json
import os
import sys
import urllib.request

from leet_data import REPO_ROOT, DIFFICULTY_COLOR, collect_problems

NOTIFIED_FILE = REPO_ROOT / ".leet-notified.json"

FLAVOR_LINES = [
    "Another one bites the dust.",
    "The algorithm gods are pleased.",
    "Big brain energy detected.",
    "Someone's grinding.",
    "Stack Overflow trembles.",
    "That's a wrap on this one.",
    "Adding it to the trophy shelf.",
]


def load_notified():
    if NOTIFIED_FILE.exists():
        try:
            return set(json.loads(NOTIFIED_FILE.read_text()))
        except json.JSONDecodeError:
            return set()
    return set()


def save_notified(folders):
    NOTIFIED_FILE.write_text(json.dumps(sorted(folders)))


def post_to_discord(webhook_url, problem, index, total):
    import random
    color_hex = DIFFICULTY_COLOR.get(problem["difficulty"], "999999")
    embed = {
        "title": f"✅ #{problem['number']} — {problem['title']}",
        "url": f"https://leetcode.com/problems/{problem['slug']}/",
        "description": random.choice(FLAVOR_LINES),
        "color": int(color_hex, 16),
        "fields": [
            {"name": "Difficulty", "value": problem["difficulty"], "inline": True},
            {"name": "Language", "value": problem["language"] or "—", "inline": True},
            {"name": "Total solved", "value": str(total), "inline": True},
        ],
        "footer": {"text": "Leet-Collection"},
    }
    payload = json.dumps({"embeds": [embed]}).encode()
    req = urllib.request.Request(
        webhook_url, data=payload, headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"  [warn] Discord post failed for {problem['folder']}: {e}", file=sys.stderr)


def main():
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
    if not webhook_url:
        print("DISCORD_WEBHOOK_URL not set — skipping Discord notification.")
        return

    problems = collect_problems()  # cheap: leet_data caches metadata already
    notified = load_notified()
    new_ones = [p for p in problems if p["folder"] not in notified]

    if not new_ones:
        print("No new solves since last notification.")
        return

    for p in new_ones:
        post_to_discord(webhook_url, p, problems.index(p) + 1, len(problems))
        notified.add(p["folder"])

    save_notified(notified)
    print(f"Notified Discord about {len(new_ones)} new solve(s).")


if __name__ == "__main__":
    main()
