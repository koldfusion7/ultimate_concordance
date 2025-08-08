# Ultimate Hebrew & Aramaic Concordance Project

This repository serves as the foundation for an unabridged concordance and dictionary of **Biblical Hebrew**, **Biblical and Targumic Aramaic**, and **Modern Hebrew**.  It is designed to support the creation of an exhaustive dataset that links every lexical entry to every place it appears across the **Tanakh**, the **Targums**, and the **Peshitta**.  Additionally, the dataset will integrate a modern Hebrew dictionary so that one project covers the entire diachronic breadth of Hebrew.

## 📂 Repository Structure

```
├── data/
│   ├── lexicon_entries.json           # Master list of lexical entries across all corpora
│   ├── tanakh_concordance.json        # Concordance linking Tanakh verses to lexical entries
│   ├── targums_concordance.json       # Concordance linking Targum verses to lexical entries
│   ├── peshitta_concordance.json      # Concordance linking Peshitta verses to lexical entries
│   ├── modern_hebrew_dictionary.json  # Modern Hebrew dictionary entries
│   └── sources/                       # Place holders for raw sources (PDFs, modules)
│       ├── 00_README.md               # Guidelines on how to populate `sources`
│       └── ...
├── scripts/
│   ├── parse_pdf.py                   # Parses PDF lexica into structured JSON entries
│   ├── parse_esword.py                # Parses e‑Sword modules (BBLX/BBLI, DCTX/DCTI, etc.) into JSON
│   ├── create_concordance.py          # Generates concordance files for Tanakh/Targums/Peshitta
│   └── utils.py                       # Shared helper functions (tokenization, transliteration, etc.)
├── docs/
│   └── schema.md                      # Detailed specification of the JSON structures
├── .gitignore
└── README.md                          # High‑level overview and project goals
```

### `data/`

All produced datasets live in this directory.  JSON is used because it is machine‑readable and integrates cleanly with modern programming environments.  Each entry in the concordance files will store references (book, chapter, verse, and word position) along with pointers to a lexical entry in `lexicon_entries.json`.

The `sources/` subdirectory **must not** be versioned with proprietary or copyrighted texts (for example, commercially licensed PDFs or premium e‑Sword modules).  Instead, this directory is where you drop your input files locally.  The parser scripts will read from here and produce JSON files in `../`.

### `scripts/`

This folder houses all the Python scripts used to convert raw input into the unified dataset:

* `parse_pdf.py` – Accepts a PDF (e.g., a scanned lexicon) and extracts entries into a structured JSON file.  It uses `pdfminer.six` for text extraction and expects that the PDF uses a consistent heading format (see `docs/schema.md` for details).
* `parse_esword.py` – Reads e‑Sword modules.  e‑Sword v9–10 modules (extensions `.bblx`, `.cmtx`, `.dctx`, `.topx`, etc.) are SQLite databases containing RTF strings.  This script uses Python’s `sqlite3` module and the `rtf_to_text` helper in `utils.py` to extract plain text.  For v11+ modules (extensions `.bbli`, `.cmti`, `.dcti`, `.refi`, etc.), the contents are stored as HTML.  The script uses `html2text` to strip markup.
* `create_concordance.py` – Once lexical entries are available and the Biblical corpora are in machine‑readable form (USFM, OSIS, etc.), this script tokenizes each verse, normalizes each word (with appropriate lemmatization), and records references back to the lexicon.
* `utils.py` – Shared functionality (e.g., Unicode normalization, transliteration helpers, gematria calculation stubs).

## 🚀 Getting Started

1. **Clone the repository:**

   ```bash
   git clone <your‑fork‑url>
   cd ultimate_concordance
   ```

2. **Install dependencies:**  The scripts rely on Python 3.9+ and some external libraries (see `requirements.txt`).  You can install them with:

   ```bash
   pip install -r requirements.txt
   ```

3. **Place source files:**  Put your PDF lexicon(s), e‑Sword modules, and any other raw sources into `data/sources/`.  The names of these files must be referenced when you run the scripts.  Do **not** commit those proprietary sources to version control.

4. **Run the parsers:**  Examples:

   ```bash
   # Convert a lexicon PDF into JSON
   python scripts/parse_pdf.py --input data/sources/my_lexicon.pdf --output data/lexicon_entries.json

   # Convert e‑Sword dictionary modules into JSON
   python scripts/parse_esword.py --input data/sources/my_dictionary.dctx --output data/modern_hebrew_dictionary.json

   # Generate concordances once all corpora are available as plain text
   python scripts/create_concordance.py --tanakh data/sources/tanakh.usfm --targums data/sources/targum.osis --peshitta data/sources/peshitta.usfm
   ```

5. **Review and iterate:**  Inspect the generated JSON files to ensure the schema meets your needs.  Contributions and improvements are welcome!

## 📖 Schema Overview

See `docs/schema.md` for a detailed specification of the JSON formats used throughout the project.  Each lexical entry includes fields such as `lemma`, `language` (Hebrew or Aramaic), `definitions`, `pos` (part of speech), `etymology`, and `modern_equivalent` when applicable.  Concordance entries consist of `lemma_id` (foreign key to the lexicon), `source` (Tanakh, Targum, Peshitta), `reference` (book, chapter, verse), and `occurrence_indices` (0‑based positions of the lemma within the verse).

## ⚠️ Licensing and Copyright

This repository itself only contains **code** and **open data** (e.g., schema definitions, demonstration snippets).  When working with copyrighted sources (commercial dictionaries or translations), you must obtain proper permission before including them in a public dataset.  The parsers are provided as a tool for **personal or scholarly use** and are not meant to distribute proprietary content.

## 🛠️ Future Work

* Implement gematria calculation methods in `utils.py` (Hebrew ordinal, standard, reduced, Atbash, etc.), and integrate them into the lexical entries.
* Add a web UI for browsing the concordance and dictionary.
* Expand `parse_pdf.py` to handle OCR of scanned documents via `pytesseract` when text extraction fails.

---

🙏 **Thank you for contributing to this important project.**  May this work serve as a valuable resource for scholars and students seeking to study the Tanakh, Targums, Peshitta, and modern Hebrew in depth.