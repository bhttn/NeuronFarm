"""
md_index.py — Markdown Index Generator

Scans a folder for .md files, reads YAML front matter, and writes a sorted
index.md into the target folder.

Usage:
    python md_index.py <folder_path>
"""

import sys
import os
from pathlib import Path
from datetime import date, datetime

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install it with: pip install pyyaml")
    sys.exit(1)

OUTPUT_FILENAME = "index.md"


def parse_front_matter(file_path: Path) -> dict:
    """Read and parse YAML front matter from a markdown file."""
    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Warning: Could not read '{file_path.name}': {e}")
        return {}

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    end_index = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = i
            break

    if end_index is None:
        return {}

    yaml_block = "\n".join(lines[1:end_index])
    try:
        data = yaml.safe_load(yaml_block)
        return data if isinstance(data, dict) else {}
    except yaml.YAMLError as e:
        print(f"Warning: Malformed YAML front matter in '{file_path.name}': {e}")
        return {}


def coerce_date(value) -> date | None:
    """Convert various date representations to a date object for sorting."""
    if value is None:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y"):
            try:
                return datetime.strptime(value.strip(), fmt).date()
            except ValueError:
                continue
    return None


def format_stars(value) -> str:
    """Return a string representation of the stars value."""
    if value is None:
        return ""
    return str(value)


def format_date(value) -> str:
    """Return a string representation of the date value."""
    if value is None:
        return ""
    if isinstance(value, (date, datetime)):
        return value.strftime("%Y-%m-%d")
    return str(value)


def sort_key(record: dict):
    """
    Sort by:
      1. rating descending (None → lowest)
      2. date descending (None → oldest)
    """
    rating = record.get("rating")
    date_val = coerce_date(record.get("date"))

    # Rating: None sorts after all real values
    rating_key = (0, -rating) if rating is not None else (1, 0)

    # Date: None sorts after all real dates
    if date_val is not None:
        date_key = (0, -date_val.toordinal())
    else:
        date_key = (1, 0)

    return (rating_key, date_key)


def build_table_row(record: dict, include_author: bool) -> str:
    title = record["title"]
    filename = record["filename"]
    stars = format_stars(record.get("stars"))
    date_str = format_date(record.get("date"))
    encoded_filename = filename.replace(" ", "%20")
    link = f"[{title}]({encoded_filename})"

    if include_author:
        author = record.get("author") or ""
        return f"| {link} | {author} | {stars} | {date_str} |"
    else:
        return f"| {link} | {stars} | {date_str} |"


def main():
    if len(sys.argv) < 2:
        print("Usage: python md_index.py <folder_path>")
        sys.exit(1)

    folder = Path(sys.argv[1])

    if not folder.exists() or not folder.is_dir():
        print(f"Error: Folder not found: {folder}")
        sys.exit(1)

    output_path = folder / OUTPUT_FILENAME

    # Discover .md files, skipping the output file
    md_files = sorted(
        [
            f for f in folder.iterdir()
            if f.is_file()
            and f.suffix.lower() == ".md"
            and f.name.lower() != OUTPUT_FILENAME.lower()
        ],
        key=lambda f: f.name.lower(),
    )

    if not md_files:
        print(f"No .md files found in '{folder}'. Nothing to do.")
        sys.exit(0)

    # Parse all files
    records = []
    for md_file in md_files:
        front_matter = parse_front_matter(md_file)
        title = front_matter.get("title") or md_file.stem
        records.append(
            {
                "filename": md_file.name,
                "title": str(title),
                "author": front_matter.get("Author"),
                "rating": front_matter.get("rating"),
                "date": front_matter.get("Date"),
                "stars": front_matter.get("stars"),
            }
        )

    # Sort
    records.sort(key=sort_key)

    # Determine whether to include the Author column
    include_author = any(r.get("author") for r in records)

    # Build output
    folder_name = folder.name
    lines = [
        "---",
        f"title: {folder_name}",
        "---",
        "",
    ]

    if include_author:
        lines.append("| Title | Author | Rating | Date |")
        lines.append("|---|---|--:|---|")
    else:
        lines.append("| Title | Rating | Date |")
        lines.append("|---|--:|---|")

    for record in records:
        lines.append(build_table_row(record, include_author))

    output_text = "\n".join(lines) + "\n"
    output_path.write_text(output_text, encoding="utf-8")
    print(f"Written: {output_path}")


if __name__ == "__main__":
    main()
