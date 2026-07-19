# -*- coding: utf-8 -*-

import argparse
import difflib
from pathlib import Path
import re
import sys

import mdformat


MARKDOWN_EXTENSIONS = {'.md', '.markdown'}
MDFORMAT_OPTIONS = {'number': True, 'wrap': 'no'}
JINJA_LINK_RE = re.compile(
    r'\\?\[(?P<label>[^\]\n]+?)\\?\]'
    r'(?P<destination>\(\s*\{\{\s*[^()\n]+?\s*\}\}\s*\))'
)

def markdown_paths(paths):
    result = []
    for path in paths:
        path = Path(path)
        if path.is_dir():
            result.extend(
                file_path
                for file_path in path.rglob('*')
                if file_path.is_file() and file_path.suffix in MARKDOWN_EXTENSIONS
            )
        elif path.is_file() and path.suffix in MARKDOWN_EXTENSIONS:
            result.append(path)
        else:
            raise SystemExit(f'Ne estas Markdown-dosiero aŭ dosierujo: {path}')
    return sorted(set(result))


def protect_jinja_links(text):
    replacements = []

    def replace_link(match):
        placeholder = f'https://mdformat.invalid/jinja-link-{len(replacements)}'
        destination = match.group('destination')[1:-1]
        replacements.append((placeholder, destination))
        return f'[{match.group("label")}]({placeholder})'

    return JINJA_LINK_RE.sub(replace_link, text), replacements


def restore_jinja_links(text, replacements):
    for placeholder, destination in replacements:
        text = text.replace(placeholder, destination)
    return text


def normalized_text(path):
    old_text = path.read_text(encoding='utf-8-sig')
    prepared_text, jinja_links = protect_jinja_links(old_text)
    new_text = mdformat.text(
        prepared_text,
        options=MDFORMAT_OPTIONS,
    )
    new_text = restore_jinja_links(new_text, jinja_links)
    return new_text if new_text.endswith('\n') else new_text + '\n'


def print_diff(path, old_text, new_text):
    diff = difflib.unified_diff(
        old_text.splitlines(keepends=True),
        new_text.splitlines(keepends=True),
        fromfile=str(path),
        tofile=str(path),
    )
    sys.stdout.writelines(diff)


def normalize_file(path, check=False, show_diff=False):
    old_text = path.read_text(encoding='utf-8-sig')
    new_text = normalized_text(path)
    if old_text == new_text:
        return False

    if show_diff:
        print_diff(path, old_text, new_text)

    if not check:
        path.write_text(new_text, encoding='utf-8')

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Normaligas Markdown-dosierojn per mdformat.'
    )
    parser.add_argument(
        'paths',
        nargs='*',
        default=['enhavo'],
        help='Markdown-dosieroj aŭ dosierujoj; defaŭlte: enhavo',
    )
    parser.add_argument(
        '--kontrolu',
        '--check',
        action='store_true',
        dest='check',
        help='nur kontrolas, ĉu dosieroj jam estas normaligitaj',
    )
    parser.add_argument(
        '--diferenco',
        '--diff',
        action='store_true',
        dest='show_diff',
        help='montras unuecan diferencon por ŝanĝotaj dosieroj',
    )
    args = parser.parse_args()

    changed = []
    errors = []
    files = markdown_paths(args.paths)
    for path in files:
        try:
            if normalize_file(path, check=args.check, show_diff=args.show_diff):
                changed.append(path)
        except (OSError, UnicodeError, ValueError) as error:
            errors.append((path, error))

    if errors:
        print('Ne eblis normaligi kelkajn Markdown-dosierojn:', file=sys.stderr)
        for path, error in errors:
            print(f'  {path}: {error}', file=sys.stderr)
        raise SystemExit(2)

    if args.check and changed:
        print('Nenormaligitaj Markdown-dosieroj:', file=sys.stderr)
        for path in changed:
            print(f'  {path}', file=sys.stderr)
        raise SystemExit(1)

    verb = 'Ŝanĝiĝus' if args.check else 'Normaligis'
    for path in changed:
        print(f'{verb}: {path}')
    print(f'Kontrolis {len(files)} Markdown-dosierojn; ŝanĝoj: {len(changed)}')


if __name__ == '__main__':
    main()
