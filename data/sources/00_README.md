# Sources Directory

This directory is intentionally left empty in the repository.  It is where you should place the **raw data sources** used to generate the concordance and lexicon.

## What to Put Here

1. **Lexicon PDFs** – Large scanned dictionaries or lexica (e.g., a 200+ MB PDF of a Hebrew lexicon).  These files will be processed by `scripts/parse_pdf.py`.
2. **e-Sword Modules** – Files with extensions like `.bblx`, `.bbli`, `.dctx`, `.dcti`, `.cmtx`, etc.  These are SQLite databases containing Bibles, commentaries, dictionaries, or books used by e-Sword.  They will be processed by `scripts/parse_esword.py`.
3. **Biblical Corpora** – Machine-readable texts of the Tanakh, Targums, and Peshitta.  Preferred formats are USFM or OSIS because they preserve verse boundaries.  These files are inputs to `scripts/create_concordance.py`.

## What **Not** to Put Here

* **No proprietary content should be committed** to the repository.  If you do not have permission to distribute a source file publicly, do not add it to version control.  Only keep it locally in this directory.

* **No generated JSON files.**  The output of your parsers (e.g., `lexicon_entries.json`) should be stored one level above (`data/`) and *should* be committed once you have cleared any licensing issues.

## Managing Large Files

If your source files are very large (hundreds of megabytes), consider splitting them into smaller chunks before uploading them to a shared drive or repository.  The parsing scripts read the files sequentially, so splitting and recombining with `cat` or `concat` tools will not affect the result.

For example, on Linux:

```bash
split -b 50m big_lexicon.pdf big_lexicon_part_

# To reassemble later:
cat big_lexicon_part_* > big_lexicon.pdf
```

Alternatively, you can host the files on a cloud storage service and point the parser scripts to the downloaded location.
