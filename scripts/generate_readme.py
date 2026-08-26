#!/usr/bin/env python3
"""
generate_readme.py
-------------------
Builds README.md from the shared problem data in leet_data.py: badges,
a live LeetCode stats card, quickchart.io charts, a trophy case, and
the full solved-problems table. Meant to be re-run automatically by
.github/workflows/update-readme.yml on every push.
"""

import json
import os
import urllib.parse
from datetime import datetime, timezone

from leet_data import (
    REPO_ROOT, DIFFICULTY_COLOR, DIFFICULTY_EMOJI,
    collect_problems, compute_achievements,
)


def quickchart_pie_url(counts):
    config = {
        "type": "doughnut",
        "data": {"labels": list(counts.keys()),
                  "datasets": [{"data": list(counts.values()),
                                "backgroundColor": [f"#{DIFFICULTY_COLOR.get(k, '999999')}" for k in counts]}]},
        "options": {"plugins": {
            "legend": {"labels": {"color": "gray", "font": {"size": 14}}},
            "title": {"display": True, "text": "Solved by Difficulty", "color": "gray"}}},
    }
    return f"https://quickchart.io/chart?c={urllib.parse.quote(json.dumps(config))}&backgroundColor=transparent&width=380&height=260"


def quickchart_topics_url(topic_counts, top_n=8):
    top = sorted(topic_counts.items(), key=lambda kv: -kv[1])[:top_n]
    if not top:
        return None
    config = {
        "type": "bar",
        "data": {"labels": [t for t, _ in top],
                  "datasets": [{"label": "Problems", "data": [c for _, c in top], "backgroundColor": "#5865F2"}]},
        "options": {"indexAxis": "y",
                     "plugins": {"legend": {"display": False},
                                 "title": {"display": True, "text": "Top Topics", "color": "gray"}},
                     "scales": {"x": {"ticks": {"color": "gray"}}, "y": {"ticks": {"color": "gray"}}}},
    }
    return f"https://quickchart.io/chart?c={urllib.parse.quote(json.dumps(config))}&backgroundColor=transparent&width=420&height=280"


def badge(label, message, color):
    return (f"https://img.shields.io/badge/{urllib.parse.quote(label)}-"
            f"{urllib.parse.quote(str(message))}-{color}?style=for-the-badge")


def build_readme(problems):
    repo = os.environ.get("GITHUB_REPOSITORY", "shritej1808/Leet-Collection")
    username = os.environ.get("LEETCODE_USERNAME", "").strip()
    pages_url = os.environ.get("PAGES_URL", "").strip()

    total = len(problems)
    diff_counts = {"Easy": 0, "Medium": 0, "Hard": 0}
    topic_counts = {}
    for p in problems:
        if p["difficulty"] in diff_counts:
            diff_counts[p["difficulty"]] += 1
        for t in p["topics"]:
            topic_counts[t] = topic_counts.get(t, 0) + 1

    achievements = compute_achievements(problems)
    unlocked = [a for a in achievements if a["unlocked"]]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = []
    lines.append(
        "<h1 align=\"center\">🧠 Leet-Collection</h1>\n"
        "<p align=\"center\">Auto-generated LeetCode solution archive, "
        "synced with <a href=\"https://github.com/3ba2ii/LeetSync\">LeetSync</a> "
        "and self-updating on every push.</p>\n"
    )

    if pages_url:
        lines.append(
            f'<p align="center"><a href="{pages_url}"><strong>'
            f'🌐 Browse the live dashboard →</strong></a></p>\n'
        )

    lines.append('<p align="center">')
    lines.append(f'  <img src="{badge("Solved", total, "5865F2")}" alt="total solved" />')
    lines.append(f'  <img src="{badge("Easy", diff_counts["Easy"], DIFFICULTY_COLOR["Easy"])}" />')
    lines.append(f'  <img src="{badge("Medium", diff_counts["Medium"], DIFFICULTY_COLOR["Medium"])}" />')
    lines.append(f'  <img src="{badge("Hard", diff_counts["Hard"], DIFFICULTY_COLOR["Hard"])}" />')
    lines.append(f'  <img src="{badge("Trophies", f"{len(unlocked)}/{len(achievements)}", "FFD700")}" />')
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

    lines.append("## 🏆 Trophy Case\n")
    lines.append(f"**{len(unlocked)} / {len(achievements)}** unlocked\n")
    lines.append("| | | | |")
    lines.append("|:---:|:---:|:---:|:---:|")
    row = []
    for a in achievements:
        icon = a["icon"] if a["unlocked"] else "🔒"
        cell = f"{icon}<br/>**{a['name']}**<br/><sub>{a['desc']}</sub>"
        row.append(cell)
        if len(row) == 4:
            lines.append("| " + " | ".join(row) + " |")
            row = []
    if row:
        while len(row) < 4:
            row.append("")
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

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
            f"{emoji} {p['difficulty']} | {p['language']} | {topics_cell or '—'} | {p['date'] or '—'} |"
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
