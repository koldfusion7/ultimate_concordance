#!/usr/bin/env python3
"""
parse_esword.py
================

This script reads e‑Sword module files (dictionary formats `.dctx` and `.dcti`,
and lexicon formats `.lexx`/`.lexi`) and converts them into a JSON dictionary
compatible with the schema described in `docs/schema.md`.

e‑Sword v9–10 modules (e.g., `.dctx`) store their content as **RTF** inside an
SQLite database.  e‑Sword v11+ modules (e.g., `.dcti`) store **HTML** in
SQLite.  This script will detect the module type based on the file extension
and use appropriate extraction functions.

Usage:

    python scripts/parse_esword.py --input data/sources/my_dictionary.dctx \
        --output data/modern_hebrew_dictionary.json

Dependencies:

    pip install html2text striprtf

"""

import argparse
import json
import sqlite3
import unicodedata
from pathlib import Path
from typing import Dict, List

import html2text  # type: ignore
from striprtf.striprtf import rtf_to_text  # type: ignore


def normalize(text: str) -> str:
    return unicodedata.normalize("NFC", text).strip()


def extract_dctx(db_path: Path) -> List[Dict]:
    """Extract dictionary entries from a .dctx (RTF) module."""
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    # According to community knowledge, the table storing dictionary entries is named 'Entries'
    try:
        cursor.execute("SELECT word, definition FROM entries")
    except sqlite3.OperationalError:
        # Fallback: some modules use different casing
        cursor.execute("SELECT Word, Definition FROM Entries")
    entries: List[Dict] = []
    entry_id_counter = 1
    for word, definition_rtf in cursor.fetchall():
        word_norm = normalize(word)
        definition_plain = normalize(rtf_to_text(definition_rtf))
        entries.append({
            "id": f"MH{entry_id_counter:05d}",
            "word": word_norm,
            "definitions": [
                {
                    "gloss": definition_plain,
                    "example": ""
                }
            ],
            "biblical_lemma_ids": [],
            "pos": "",
            "notes": ""
        })
        entry_id_counter += 1
    conn.close()
    return entries


def extract_dcti(db_path: Path) -> List[Dict]:
    """Extract dictionary entries from a .dcti (HTML) module."""
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT word, definition FROM entries")
    except sqlite3.OperationalError:
        cursor.execute("SELECT Word, Definition FROM Entries")
    entries: List[Dict] = []
    entry_id_counter = 1
    h = html2text.HTML2Text()
    h.ignore_links = True
    for word, definition_html in cursor.fetchall():
        word_norm = normalize(word)
        definition_plain = normalize(h.handle(definition_html))
        entries.append({
            "id": f"MH{entry_id_counter:05d}",
            "word": word_norm,
            "definitions": [
                {
                    "gloss": definition_plain,
                    "example": ""
                }
            ],
            "biblical_lemma_ids": [],
            "pos": "",
            "notes": ""
        })
        entry_id_counter += 1
    conn.close()
    return entries


def parse_esword_module(path: Path) -> List[Dict]:
    """Determine module type and extract entries accordingly."""
    suffix = path.suffix.lower()
    if suffix == ".dctx":
        return extract_dctx(path)
    if suffix == ".dcti":
        return extract_dcti(path)
    raise ValueError(f"Unsupported module type: {suffix}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert an e‑Sword dictionary module into JSON")
    parser.add_argument("--input", required=True, help="Path to the .dctx/.dcti file")
    parser.add_argument("--output", required=True, help="Path to the output JSON file")
    args = parser.parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file {input_path} not found")
    entries = parse_esword_module(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    print(f"Extracted {len(entries)} entries from {input_path} into {output_path}")


if __name__ == "__main__":
    main()