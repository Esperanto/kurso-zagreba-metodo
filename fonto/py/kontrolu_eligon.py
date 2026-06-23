#!/usr/bin/env python

import argparse
import re
import sqlite3
import tempfile
import zipfile
from pathlib import Path


GRAMATIKO_PATTERN = re.compile(r'<div dir="ltr">\s*<h3>Alphabet</h3>')
PWA_MANIFEST_PATTERN = re.compile(r'/manifest\.webmanifest')
PWA_REGISTER_PATTERN = re.compile(r'/pwa/registru\.js')
PWA_SERVICE_WORKER_PATTERN = re.compile(r'const PRECACHE_URLS = \[')


def fail(message):
    raise SystemExit('Kontrolo malsukcesis: ' + message)


def require_nonempty_file(path):
    if not path.is_file():
        fail('mankas dosiero ' + str(path))
    if path.stat().st_size == 0:
        fail('malplenas dosiero ' + str(path))
    try:
        with path.open('rb') as handle:
            handle.read(1)
    except OSError as error:
        fail('ne eblas legi ' + str(path) + ': ' + str(error))


def require_pattern(path, pattern):
    require_nonempty_file(path)
    try:
        text = path.read_text(encoding='utf-8')
    except UnicodeDecodeError as error:
        fail('ne eblas legi kiel UTF-8 ' + str(path) + ': ' + str(error))
    if not pattern.search(text):
        fail('mankas atendita enhavo en ' + str(path))


def require_apkg(path):
    require_nonempty_file(path)
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            if 'collection.anki2' not in names:
                fail('mankas collection.anki2 en ' + str(path))
            if 'media' not in names:
                fail('mankas media en ' + str(path))
            collection = archive.read('collection.anki2')
    except zipfile.BadZipFile as error:
        fail('nevalida APKG-zip ' + str(path) + ': ' + str(error))

    with tempfile.NamedTemporaryFile(suffix='.anki2') as database:
        database.write(collection)
        database.flush()
        connection = None
        try:
            connection = sqlite3.connect(database.name)
            notes = connection.execute('select count(*) from notes').fetchone()[0]
            cards = connection.execute('select count(*) from cards').fetchone()[0]
        except sqlite3.Error as error:
            fail('ne eblas legi collection.anki2 el ' + str(path) + ': ' + str(error))
        finally:
            if connection:
                connection.close()

    if notes < 1:
        fail('APKG enhavas neniun noton: ' + str(path))
    if cards < 1:
        fail('APKG enhavas neniun karton: ' + str(path))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lingvo', required=True)
    parser.add_argument('--md-out', required=True)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()

    lingvo = args.lingvo
    output_dir = Path(args.output_dir)
    md_out = Path(args.md_out)
    lingvo_dir = output_dir / lingvo

    for path in [
        md_out,
        output_dir / 'index.html',
        lingvo_dir / 'index.html',
        output_dir / 'assets' / 'css' / 'main.css',
        output_dir / 'assets' / 'js' / 'main.js',
        output_dir / 'vendor' / 'bootstrap' / 'css' / 'bootstrap.min.css',
        output_dir / 'manifest.webmanifest',
        output_dir / 'manifest.json',
        output_dir / 'pwa' / 'registru.js',
        output_dir / 'pwa' / 'images' / 'ecbc30ce-3901-d33d-412d-10551879846f.webPlatform.png',
        output_dir / 'sw.js',
    ]:
        require_nonempty_file(path)

    require_pattern(output_dir / 'index.html', PWA_MANIFEST_PATTERN)
    require_pattern(output_dir / 'index.html', PWA_REGISTER_PATTERN)
    require_pattern(lingvo_dir / 'index.html', PWA_MANIFEST_PATTERN)
    require_pattern(lingvo_dir / 'index.html', PWA_REGISTER_PATTERN)
    require_pattern(output_dir / 'sw.js', PWA_SERVICE_WORKER_PATTERN)
    require_pattern(lingvo_dir / '01' / 'gramatiko' / 'index.html', GRAMATIKO_PATTERN)
    require_apkg(lingvo_dir / 'eksporto' / (lingvo + '.apkg'))

    print('Sukcesis: kontrolis Markdown-, HTML- kaj Anki-eligon por ' + lingvo)


if __name__ == '__main__':
    main()
