#!/usr/bin/env python3
"""
Revert whitespace-only formatting changes while preserving real textual edits.

This script compares modified tracked files against HEAD, identifies changes that
differ only in whitespace, and reverts those to HEAD while keeping all substantive
textual changes. Useful for undoing format-on-save artifacts.

Usage:
    python3 revert_whitespace_only.py
"""

import os
import re
import subprocess
import sys
from difflib import SequenceMatcher


def run(cmd):
    return subprocess.check_output(cmd, stderr=subprocess.DEVNULL)


def is_binary(data: bytes) -> bool:
    return b"\0" in data


def normalize_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def main():
    # get modified tracked files
    try:
        out = run(["git", "ls-files", "-m"]).decode("utf-8")
    except Exception as e:
        print("error: git failed", e)
        sys.exit(2)

    files = [ln for ln in out.splitlines() if ln]
    if not files:
        print("No modified tracked files found.")
        return

    changed = []

    for path in files:
        # skip if file removed in working tree
        if not os.path.exists(path):
            continue

        with open(path, "rb") as f:
            work_bytes = f.read()

        if is_binary(work_bytes):
            print(f"Skipping binary file: {path}")
            continue

        work_text = work_bytes.decode("utf-8", "surrogateescape")

        # get HEAD content
        try:
            head_bytes = run(["git", "show", f"HEAD:{path}"])
        except subprocess.CalledProcessError:
            # file not present in HEAD (new file) -> skip
            continue

        if is_binary(head_bytes):
            print(f"Skipping binary file in HEAD: {path}")
            continue

        head_text = head_bytes.decode("utf-8", "surrogateescape")

        if head_text == work_text:
            continue

        head_lines = head_text.splitlines(keepends=True)
        work_lines = work_text.splitlines(keepends=True)

        sm = SequenceMatcher(None, head_lines, work_lines)
        out_lines = []

        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                out_lines.extend(work_lines[j1:j2])
            else:
                head_chunk = "".join(head_lines[i1:i2])
                work_chunk = "".join(work_lines[j1:j2])
                if normalize_ws(head_chunk) == normalize_ws(work_chunk):
                    # only whitespace differences -> revert to HEAD chunk
                    out_lines.append(head_chunk)
                else:
                    # real change: keep working chunk
                    out_lines.append(work_chunk)

        merged = "".join(out_lines)

        if merged != work_text:
            # write back
            with open(path, "wb") as f:
                f.write(merged.encode("utf-8", "surrogateescape"))
            changed.append(path)

    if changed:
        print("Reverted whitespace-only changes for:")
        for p in changed:
            print(" -", p)
    else:
        print("No whitespace-only edits to revert.")


if __name__ == "__main__":
    main()
