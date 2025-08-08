#!/usr/bin/env python3
"""
parse_pdf.py
===============

This script converts a lexicon contained in a PDF file into a structured JSON file
compatible with the schema defined in `docs/schema.md`.  Because each lexicon
has its own formatting conventions, this script provides a generic pipeline and
tries to be as modular as possible.  You will likely need to tweak the regex
patterns and heuristics to suit your specific source.

Usage:

    python scripts/parse_pdf.py --input data/sources/lexicon.pdf \
        --output data/lexicon_entries.json

Dependencies:

    pip install pdfminer.six

Notes:

* For scanned PDFs without embedded text, you will need OCR.  The script
  currently does not perform OCR automatically.  You can integrate
  `pytesseract` or another OCR engine if needed.
* This script assumes the PDF uses a heading format where each entry begins
  with the lemma in bold or uppercase, followed by definitions.  Adjust
  `ENTRY_PATTERN` accordingly.
"""

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import List, Dict, Iterator

from pdfminer.high_level import extract_text


def normalize(text: str) -> str:
    """Normalize Hebrew/Aramaic text to NFC and strip extraneous whitespace."""
    return unicodedata.normalize("NFC", text).strip()


def iter_entries(text: str) -> Iterator[Dict]:
    """Yield lexical entries from the extracted PDF text.

    The default implementation uses a very simple regular expression to
    identify entries.  You will need to modify this pattern to match the
    structure of your lexicon.  Each entry should produce a dictionary
    following the `lexicon_entries.json` schema.
    """
    # Example pattern: lines that start with a Hebrew or Aramaic word (letters
    # from Unicode ranges U+0590–U+05FF) followed by a space and then a
    # definition.  This is just a placeholder; adapt as needed.
    entry_pattern = re.compile(r"^([\u0590-\u05FF]+)\s+(.+)$", re.MULTILINE)
    entry_id_counter = 1
    for match in entry_pattern.finditer(text):
        lemma = normalize(match.group(1))
        definition = match.group(2).strip()
        # Build an entry.  At minimum we need id, lemma, language and definitions.
        entry = {
            "id": f"LEX{entry_id_counter:05d}",
            "lemma": lemma,
            "language": "Hebrew",  # or detect based on script or user input
            "pos": "unknown",
            "definitions": [
                {
                    "gloss": definition,
                    "source": "PDF Lexicon"
                }
            ],
            "etymology": "",
            "related_forms": [],
            "modern_equivalent": "",
            "notes": ""
        }
        entry_id_counter += 1
        yield entry


def parse_pdf(pdf_path: Path) -> List[Dict]:
    """Extract text from a PDF and return a list of entries."""
    print(f"Extracting text from {pdf_path}...")
    text = extract_text(str(pdf_path))
    print("Text extraction complete.  Parsing entries...")
    entries = list(iter_entries(text))
    print(f"Parsed {len(entries)} entries.")
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a lexicon PDF into JSON")
    parser.add_argument("--input", required=True, help="Path to the input PDF file")
    parser.add_argument("--output", required=True, help="Path to the output JSON file")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file {input_path} does not exist")

    entries = parse_pdf(input_path)
    # Write to JSON
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(entries)} entries to {output_path}")


if __name__ == "__main__":
    main()