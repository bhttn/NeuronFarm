"""
generate_index.py

Recursively scans a target folder and creates an index.md in each folder
containing standard Markdown links to all .md files, organised by
subfolder hierarchy using Markdown headings.

Link format:
    [FileName](./FileName.md)
    [FileName](./SubFolder/FileName.md)

Usage:
    python generate_index.py "<path_to_target_folder>"
"""

import argparse
import os
import sys


def get_md_files(folder: str) -> list[str]:
    """Return sorted list of .md filenames (excluding index.md) in folder."""
    try:
        entries = os.listdir(folder)
    except PermissionError:
        return []
    return sorted(
        [f for f in entries
         if f.lower().endswith(".md") and f.lower() != "index.md"
         and os.path.isfile(os.path.join(folder, f))],
        key=str.casefold
    )


def get_subfolders(folder: str) -> list[str]:
    """Return sorted list of subfolder names in folder."""
    try:
        entries = os.listdir(folder)
    except PermissionError:
        return []
    return sorted(
        [f for f in entries if os.path.isdir(os.path.join(folder, f))],
        key=str.casefold
    )


def folder_has_md(folder: str) -> bool:
    """Return True if folder or any descendant contains a non-index .md file."""
    for root, dirs, files in os.walk(folder):
        dirs.sort(key=str.casefold)
        for f in files:
            if f.lower().endswith(".md") and f.lower() != "index.md":
                return True
    return False


def make_link(label: str, rel_prefix: str, filename: str) -> str:
    """
    Build a standard Markdown link.

    label:      display text (filename without extension)
    rel_prefix: forward-slash path prefix relative to the index.md (starts as ".")
    filename:   the .md filename
    Returns e.g. [File1](./File1.md) or [File1](./SubFolder/File1.md)
    """
    path = rel_prefix + "/" + filename
    return f"[{label}]({path})"


def build_index_lines(folder: str, rel_prefix: str = ".", depth: int = 1) -> list[str]:
    """
    Recursively build the lines for an index.md rooted at `folder`.

    rel_prefix: the relative path prefix used in links (starts as ".")
    depth:      heading depth for subfolders (## = depth 2, so start at 1
                so the first subfolder level gets ##)
    """
    lines = []

    # Files directly in this folder (no heading)
    md_files = get_md_files(folder)
    for f in md_files:
        label = os.path.splitext(f)[0]
        lines.append(make_link(label, rel_prefix, f))

    # Subfolders
    subfolders = get_subfolders(folder)
    for sf in subfolders:
        sf_path = os.path.join(folder, sf)
        if not folder_has_md(sf_path):
            continue

        heading = "#" * (depth + 1)  # depth=1 → ##, depth=2 → ###, etc.
        lines.append("")
        lines.append(f"{heading} {sf}")

        sf_prefix = rel_prefix + "/" + sf
        child_lines = build_index_lines(sf_path, sf_prefix, depth + 1)
        lines.extend(child_lines)

    return lines


def write_index(folder: str) -> bool:
    """Write index.md for a single folder. Returns True on success."""
    lines = build_index_lines(folder)

    # Strip leading blank lines
    while lines and lines[0] == "":
        lines.pop(0)

    content = "\n".join(lines)
    if content and not content.endswith("\n"):
        content += "\n"

    index_path = os.path.join(folder, "index.md")
    try:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except PermissionError:
        print(f"  WARNING: Cannot write to {index_path} — permission denied.", file=sys.stderr)
        return False


def generate_all_indexes(root: str) -> list[str]:
    """
    Walk the tree and write index.md in every folder that contains
    (directly or indirectly) at least one non-index .md file.
    Returns list of paths where index.md was successfully written.
    """
    created = []

    for dirpath, dirnames, _ in os.walk(root):
        dirnames.sort(key=str.casefold)
        if folder_has_md(dirpath):
            if write_index(dirpath):
                created.append(os.path.join(dirpath, "index.md"))

    return created


def main():
    parser = argparse.ArgumentParser(
        description="Generate Markdown index.md files in a folder tree."
    )
    parser.add_argument("target", help="Path to the root folder to index")
    args = parser.parse_args()

    target = os.path.abspath(args.target)

    if not os.path.exists(target):
        print(f"Error: Folder does not exist: {target}", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(target):
        print(f"Error: Path is not a folder: {target}", file=sys.stderr)
        sys.exit(1)

    created = generate_all_indexes(target)

    print(f"\nIndex files created: {len(created)}")
    for path in created:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
