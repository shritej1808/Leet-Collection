#!/usr/bin/env python3
"""
generate_site.py
-----------------
Builds docs/data.json for the static dashboard site (docs/index.html +
docs/assets/*). GitHub Pages serves the docs/ folder directly — the
site is plain HTML/CSS/JS with no build step, so this script's only
job is to drop fresh data next to it.

Run by the same GitHub Action as generate_readme.py, right after it.
"""

import json
import os
from datetime import datetime, timezone

from leet_data import REPO_ROOT, collect_problems, compute_achievements

DOCS_DIR = REPO_ROOT / "docs"


def main():
    problems = collect_problems()
    achievements = compute_achievements(problems)
    repo = os.environ.get("GITHUB_REPOSITORY", "shritej1808/Leet-Collection")

    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "repo": repo,
        "problems": [
            {
                "number": p["number"],
                "slug": p["slug"],
                "folder": p["folder"],
                "title": p["title"],
                "difficulty": p["difficulty"],
                "topics": p["topics"],
                "languages": p["languages"],
                "solution_file": p["solution_file"],
                "date": p["date"],
                "raw_url": (
                    f"https://raw.githubusercontent.com/{repo}/main/"
                    f"{p['folder']}/{p['solution_file']}"
                    if p["solution_file"] else None
                ),
                "github_url": f"https://github.com/{repo}/tree/main/{p['folder']}",
                "leetcode_url": f"https://leetcode.com/problems/{p['slug']}/",
            }
            for p in problems
        ],
        "achievements": achievements,
    }

    DOCS_DIR.mkdir(exist_ok=True)
    (DOCS_DIR / "data.json").write_text(json.dumps(data, indent=2))
    print(f"Wrote docs/data.json with {len(problems)} problems.")


if __name__ == "__main__":
    main()
