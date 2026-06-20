# AGENTS.md

Guidance for automated coding agents working in this repository.

## Project Overview

This repository contains the Esperanto course according to the Zagreb method. The course content is stored mostly as YAML and Markdown, then rendered to HTML, Markdown, PDF, EPUB, or related formats.

The project language and user-facing documentation are primarily Esperanto. Preserve existing Esperanto wording and filename conventions unless a task explicitly asks for translation or copy changes.

## Important Directories

- `enhavo/netradukenda/`: non-translatable source content shared by all languages.
- `enhavo/netradukenda/tekstoj/`: Esperanto lesson texts. These are licensed CC BY-ND and must not be changed.
- `enhavo/tradukenda/<lingvo>/`: language-specific translations, grammar notes, exercises, dictionaries, intro, and outro text.
- `agordoj/`: language and author configuration.
- `html_generiloj/`: HTML generation code, templates, and generated output.
- `leo_markdown/`: Markdown generation code and templates.
- `genanki/`: bundled or vendored Anki-related project; avoid touching it unless the task is specifically about that subtree.

## Setup And Commands

Install Python dependencies with:

```sh
pip install -r requirements.txt
```

Generate HTML for a language, for example English:

```sh
python generate.py --lingvo en --eligformo html
```

This writes to `html_generiloj/output/en`.

Generate Markdown:

```sh
python generate.py --lingvo en --eligformo md
```

The Markdown output is written to stdout. PDF and EPUB generation require Pandoc, as described in `README.md`.

## Editing Content

- Keep YAML valid and prefer existing nearby structure over introducing new formats.
- Quote YAML values that may be interpreted as booleans or special scalars, such as `on`, `off`, `yes`, or values containing apostrophes.
- For grammar Markdown, follow the conventions in `KONTRIBUADO.md`: Esperanto examples use `*...*`, translations are separated with `–`, and highlighted morphemes use `__...__`.
- When adding or updating a language, mirror the existing directory shape under `enhavo/tradukenda/`.
- Do not modify `enhavo/netradukenda/tekstoj/` unless the user explicitly confirms a license-aware change.

## Code Style Notes

- This is a small Python project using simple modules and Jinja/Chevron-style templates. Prefer straightforward changes over new abstractions.
- Preserve UTF-8 text and Esperanto diacritics.
- `generate.py` is the main entry point and expects to be run from the repository root.
- Avoid committing generated caches such as `__pycache__/` or `.pyc` files.

## Validation

There is no root-level automated test suite documented. For generator or template changes, run at least:

```sh
python generate.py --lingvo en --eligformo html
```

For Markdown-output changes, also run:

```sh
python generate.py --lingvo en --eligformo md >/tmp/leo-en.md
```

If a change affects a specific language, run the generator for that language too.
