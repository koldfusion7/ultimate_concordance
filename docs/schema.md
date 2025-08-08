# JSON Schema Definitions

This document outlines the expected structure for the JSON files produced by the project.  Although the schemas are not expressed using a formal JSON Schema definition language (e.g., Draft-07), the conventions described here should be followed to ensure consistency and interoperability.

## `lexicon_entries.json`

This file is an **array** of objects, each representing a unique lexical entry across Hebrew or Aramaic.  The order of entries is not significant; however, each object must contain a unique `id` that will be referenced by the concordance files.

```json
{
  "id": "H0001",
  "lemma": "אָב",
  "language": "Hebrew",
  "pos": "noun",
  "definitions": [
    {
      "gloss": "father",
      "source": "Lexicon Name"
    },
    {
      "gloss": "ancestor",
      "source": "Another Lexicon"
    }
  ],
  "etymology": "From the root א‌-ב meaning to will or desire",
  "related_forms": ["אבים", "אבינו"],
  "modern_equivalent": "אָב‎ (modern Hebrew spelling)",
  "notes": "Any additional remarks about the entry"
}
```

* **`id`** – A unique identifier for the lemma.  It should combine a prefix (e.g., `H` for Hebrew, `A` for Aramaic) with a numeric code.  This is used as a foreign key in concordance files.
* **`lemma`** – The canonical spelling of the word as found in standard lexica.
* **`language`** – Either `Hebrew` or `Aramaic`.
* **`pos`** – Part of speech.  Use standard labels (`noun`, `verb`, `adj`, etc.).
* **`definitions`** – An array of sense objects.  Each definition includes a plain-language gloss and the lexicon or dictionary from which it was derived.
* **`etymology`** – A string describing the historical origin of the word.  Include references to roots when possible.
* **`related_forms`** – Variants or inflected forms associated with this lemma.  These forms will be used during concordance generation for matching.
* **`modern_equivalent`** – When applicable, the modern Hebrew form of the word.  Not all Biblical entries have a modern counterpart.
* **`notes`** – Free-text field for miscellaneous comments (e.g., Talmudic usage, dialectal notes).

## `tanakh_concordance.json`, `targums_concordance.json`, `peshitta_concordance.json`

Each concordance file is an **array** of objects.  Each object records one occurrence of a lemma in a particular verse.  A single verse may appear multiple times in the array if multiple lexemes occur in it.

```json
{
  "lemma_id": "H0001",
  "source": "Tanakh",
  "reference": {
    "book": "Genesis",
    "chapter": 1,
    "verse": 1
  },
  "occurrence_indices": [0]
}
```

* **`lemma_id`** – The `id` from `lexicon_entries.json`.
* **`source`** – One of `Tanakh`, `Targums`, or `Peshitta`.
* **`reference`** – An object indicating the book name, chapter number, and verse number where the lemma occurs.  Use English book names (e.g., `Genesis`, `Exodus`, `Jeremiah`).
* **`occurrence_indices`** – An array of zero-based integer indices indicating the positions within the verse token list where the lemma occurs.  A verse might contain the same lemma more than once; list all positions.

If you wish to record additional metadata (e.g., morphological tagging, strong numbers), you may extend these objects with extra fields.  The `create_concordance.py` script is designed to be extensible.

## `modern_hebrew_dictionary.json`

This file is also an **array** of objects.  The structure is similar to that of `lexicon_entries.json`, but tailored for Modern Hebrew.  Where possible, you should link a modern dictionary entry back to a Biblical lemma using the `biblical_lemma_ids` field.  Modern words that do not have a Biblical root can omit this field.

```json
{
  "id": "MH0001",
  "word": "אבא",
  "definitions": [
    {
      "gloss": "dad, father",
      "example": "אבא שלי עובד כרופא"
    }
  ],
  "biblical_lemma_ids": ["H0001"],
  "pos": "noun",
  "notes": "Common colloquial form for father"
}
```

* **`id`** – Unique identifier for the modern word, prefaced with `MH`.
* **`word`** – The modern Hebrew word.
* **`definitions`** – Array of sense objects.  Each may include a gloss and optional example sentences.
* **`biblical_lemma_ids`** – Array of lexical identifiers linking modern words to the Biblical lexicon.  Many modern words derive from Biblical roots; this linkage enables cross-era navigation.
* **`pos`** – Part of speech.
* **`notes`** – Free-text notes.

## Notes on Encoding

All JSON files must be UTF-8 encoded.  Hebrew and Aramaic strings should appear in **Unicode Normalization Form C (NFC)** to ensure consistent matching.  The `utils.py` file provides helper functions for normalization.

## Extensibility

The schemas described here are intentionally flexible.  You may add fields as needed, provided you document them and keep the core fields unchanged so that scripts depending on them continue to function.
