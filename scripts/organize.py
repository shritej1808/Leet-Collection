#!/usr/bin/env python3

import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INCOMING = ROOT / "_incoming"
DEST_ROOT = ROOT / "leetcode"

REQUIRED = ("Problem", "Difficulty", "Domain", "Date")
VALID_DIFFICULTIES = {"Easy", "Medium", "Hard"}


def read_metadata(readme):
    text = readme.read_text(encoding="utf-8")
    metadata = {}

    for key in REQUIRED:
        match = re.search(
            rf"^\s*-?\s*{re.escape(key)}\s*:\s*(.+?)\s*$",
            text,
            re.MULTILINE | re.IGNORECASE
        )

        if not match:
            raise ValueError(f"Missing metadata: {key}")

        metadata[key] = match.group(1).strip()

    if metadata["Difficulty"] not in VALID_DIFFICULTIES:
        raise ValueError("Difficulty must be Easy, Medium or Hard")

    if not re.fullmatch(r"\d+", metadata["Problem"]):
        raise ValueError("Problem must be a number")

    try:
        date.fromisoformat(metadata["Date"])
    except ValueError:
        raise ValueError("Date must use YYYY-MM-DD")

    return metadata


def slugify(value):
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def get_title(readme, fallback):
    text = readme.read_text(encoding="utf-8")

    # Existing LeetCode-generated README
    match = re.search(
        r"<h[1-6][^>]*>\s*<a[^>]*>(.*?)</a>",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        title = re.sub(r"<[^>]+>", "", match.group(1))
        if title.strip():
            return title.strip()

    # Markdown README
    match = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)

    if match:
        return match.group(1).strip()

    return fallback


def main():
    if not INCOMING.exists():
        print("No _incoming directory found.")
        return

    submissions = [
        p for p in INCOMING.iterdir()
        if p.is_dir()
    ]

    if not submissions:
        print("No submissions to organize.")
        return

    for submission in sorted(submissions):

        readme = submission / "README.md"
        java_files = list(submission.glob("*.java"))

        if not readme.exists():
            raise ValueError(
                f"{submission}: README.md missing"
            )

        if len(java_files) != 1:
            raise ValueError(
                f"{submission}: exactly one .java file required"
            )

        metadata = read_metadata(readme)

        title = get_title(readme, submission.name)

        domain = slugify(metadata["Domain"])
        title_slug = slugify(title)
        number = metadata["Problem"]

        destination = (
            DEST_ROOT
            / domain
            / f"{number}-{title_slug}"
        )

        if destination.exists():
            raise FileExistsError(
                f"Destination already exists: {destination}"
            )

        destination.mkdir(
            parents=True,
            exist_ok=False
        )

        shutil.move(
            str(java_files[0]),
            destination / java_files[0].name
        )

        shutil.move(
            str(readme),
            destination / "README.md"
        )

        submission.rmdir()

        print(
            f"✓ {submission.name} → "
            f"{destination.relative_to(ROOT)}"
        )

    print("\n✓ Organization complete.")


if __name__ == "__main__":
    main()