#!/usr/bin/env python3
"""
create_concordance.py
=====================

Generates concordance files for the Tanakh, Targums, and Peshitta based on
machine‑readable source texts.  This script expects that you have already
generated a `lexicon_entries.json` file and optionally a `modern_hebrew_dictionary.json`.

Usage:

    python scripts/create_concordance.py \
        --tanakh data/sources/tanakh.usfm \
        --targums data/sources/targum.osis \
        --peshitta data/sources/peshitta.usfm \
        --lexicon data/lexicon_entries.json \
        --output-dir data/

Dependencies:

    pip install openpyxl usfm-tools

Notes:

* This script currently includes a **very simple** tokenization and lemmatization
  approach.  It splits on whitespace and punctuation and attempts to match
  normalized words against the `lemma` values in the lexicon.  For a real
  implementation you would integrate a morphological analyzer such as
  [pymorphy2](https://github.com/kmike/pymorphy2) for Russian or adapt an
  existing Hebrew/Aramaic lemmatizer.
* It is assumed that the verse boundaries are clearly delimited in the source
  files.  USFM and OSIS formats both provide markers for book/chapter/verse.
"""

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def normalize(word: str) -> str:
    return unicodedata.normalize("NFC", word).strip()


def load_lexicon(path: Path) -> Dict[str, Dict]:
    """Load the lexicon file and build a mapping from lemma to id."""
    with path.open("r", encoding="utf-8") as f:
        entries = json.load(f)
    lemma_to_id: Dict[str, str] = {}
    for entry in entries:
        lemma = normalize(entry["lemma"])
        lemma_to_id[lemma] = entry["id"]
    return lemma_to_id


def parse_usfm(usfm_path: Path) -> List[Tuple[str, int, int, str]]:
    """Parse a USFM file and yield tuples of (book, chapter, verse, verse_text)."""
    verses = []
    current_book = None
    current_chapter = None
    current_verse = None
    verse_text_parts: List[str] = []
    usfm_re = re.compile(r"\\(\w+)\s*(.*)")
    with usfm_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = usfm_re.match(line)
            if match:
                marker, content = match.groups()
                if marker == "id":
                    current_book = content.split()[0]
                elif marker == "c":
                    if current_book is None:
                        continue
                    current_chapter = int(content)
                elif marker == "v":
                    # flush previous verse
                    if current_book and current_chapter and current_verse is not None:
                        verses.append((current_book, current_chapter, current_verse, " ".join(verse_text_parts)))
                        verse_text_parts = []
                    current_verse = int(content)
                else:
                    # other marker: ignore
                    pass
            else:
                # append to verse text
                if current_book and current_chapter and current_verse is not None:
                    verse_text_parts.append(line)
        # flush last verse
        if current_book and current_chapter and current_verse is not None:
            verses.append((current_book, current_chapter, current_verse, " ".join(verse_text_parts)))
    return verses


def tokenize(text: str) -> List[str]:
    """Tokenize a verse by splitting on whitespace and punctuation."""
    # Remove punctuation (except Hebrew cantillation marks which should be removed anyway)
    tokens = re.split(r"[\s\d\p{P}]+", text)
    return [normalize(token) for token in tokens if token]


def build_concordance(verses: List[Tuple[str, int, int, str]], lemma_to_id: Dict[str, str], source_name: str) -> List[Dict]:
    """Generate concordance entries for a list of verses."""
    concordance: List[Dict] = []
    for book, chapter, verse_num, verse_text in verses:
        tokens = tokenize(verse_text)
        for idx, token in enumerate(tokens):
            lemma_id = lemma_to_id.get(token)
            if lemma_id:
                concordance.append({
                    "lemma_id": lemma_id,
                    "source": source_name,
                    "reference": {
                        "book": book,
                        "chapter": chapter,
                        "verse": verse_num
                    },
                    "occurrence_indices": [idx]
                })
    return concordance


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate concordance files from corpus texts")
    parser.add_argument("--lexicon", required=True, help="Path to lexicon_entries.json")
    parser.add_argument("--tanakh", help="Path to Tanakh USFM file")
    parser.add_argument("--targums", help="Path to Targums OSIS or USFM file")
    parser.add_argument("--peshitta", help="Path to Peshitta USFM file")
    parser.add_argument("--output-dir", required=True, help="Directory to write concordance JSON files")
    args = parser.parse_args()

    lemma_to_id = load_lexicon(Path(args.lexicon))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.tanakh:
        print("Processing Tanakh...")
        tanakh_verses = parse_usfm(Path(args.tanakh))
        tanakh_concordance = build_concordance(tanakh_verses, lemma_to_id, "Tanakh")
        with (output_dir / "tanakh_concordance.json").open("w", encoding="utf-8") as f:
            json.dump(tanakh_concordance, f, ensure_ascii=False, indent=2)
        print(f"Wrote {len(tanakh_concordance)} concordance entries for Tanakh.")

    # Targums and Peshitta can be implemented similarly using parse_usfm or another parser
    # For demonstration, we simply skip them if not provided
    if args.targums:
        print("Processing Targums (experimental)...")
        targum_verses = parse_usfm(Path(args.targums))
        targum_concordance = build_concordance(targum_verses, lemma_to_id, "Targums")
        with (output_dir / "targums_concordance.json").open("w", encoding="utf-8") as f:
            json.dump(targum_concordance, f, ensure_ascii=False, indent=2)
        print(f"Wrote {len(targum_concordance)} concordance entries for Targums.")

    if args.peshitta:
        print("Processing Peshitta...")
        peshitta_verses = parse_usfm(Path(args.peshitta))
        peshitta_concordance = build_concordance(peshitta_verses, lemma_to_id, "Peshitta")
        with (output_dir / "peshitta_concordance.json").open("w", encoding="utf-8") as f:
            json.dump(peshitta_concordance, f, ensure_ascii=False, indent=2)
        print(f"Wrote {len(peshitta_concordance)} concordance entries for Peshitta.")


if __name__ == "__main__":
    main()
