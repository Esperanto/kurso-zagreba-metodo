#!/usr/bin/env python

import argparse
import re
import sqlite3
import tempfile
import zipfile
from pathlib import Path


GRAMATIKO_PATTERN = re.compile(r'<h3 id="alphabet">Alphabet</h3>')
GRAMATIKO_TOC_PATTERN = re.compile(
    r'<nav id="gramatika-enhavtabelo" class="gramatika-enhavtabelo"[^>]*>.*'
    r'<a href="#alphabet">Alphabet</a>.*'
    r'<a href="#pronunciation">Pronunciation</a>',
    re.S,
)
GRAMATIKO_EMFAZO_PATTERN = re.compile(r'<em>labor<strong>i</strong></em>\s+–\s+to work')
BOOTSTRAP_PATTERN = re.compile(r'Bootstrap\s+v5\.3\.8')
JQUERY_PATTERN = re.compile(r'jQuery v3\.7\.1')
TYPEAHEAD_PATTERN = re.compile(r'typeahead\.js 0\.11\.1')
HTML_LANG_PATTERN = re.compile(r'<html lang="en" dir="ltr" translate="no">')
TITLE_ROOT_PATTERN = re.compile(r'<title>Learn Esperanto \| The Fastest Basics Course</title>')
META_DESCRIPTION_PATTERN = re.compile(r'<meta name="description" content="Teaches the most important 500 words\. Free and without registration\.')
CANONICAL_ROOT_PATTERN = re.compile(r'<link rel="canonical" href="https://esperanto12\.net/en/" />')
CANONICAL_LESSON_PATTERN = re.compile(r'<link rel="canonical" href="https://esperanto12\.net/en/01/" />')
HREFLANG_EN_PATTERN = re.compile(r'<link rel="alternate" hreflang="en" href="https://esperanto12\.net/en/" />')
HREFLANG_DE_PATTERN = re.compile(r'<link rel="alternate" hreflang="de" href="https://esperanto12\.net/de/" />')
HREFLANG_X_DEFAULT_PATTERN = re.compile(r'<link rel="alternate" hreflang="x-default" href="https://esperanto12\.net/" />')
OG_URL_ROOT_PATTERN = re.compile(r'<meta property="og:url" content="https://esperanto12\.net/en/" />')
OG_URL_LESSON_PATTERN = re.compile(r'<meta property="og:url" content="https://esperanto12\.net/en/01/" />')
OG_SITE_NAME_PATTERN = re.compile(r'<meta property="og:site_name" content="Esperanto12\.net" />')
OG_DESCRIPTION_PATTERN = re.compile(r'<meta property="og:description" content="Teaches the most important 500 words\. Free and without registration\.')
OG_LOCALE_EN_PATTERN = re.compile(r'<meta property="og:locale" content="en_US" />')
OG_LOCALE_ALTERNATE_DE_PATTERN = re.compile(r'<meta property="og:locale:alternate" content="de_DE" />')
OG_AUDIO_PATTERN = re.compile(r'<meta property="og:audio" content="https://esperanto12\.net/assets/ogg/01\.ogg" />')
OG_AUDIO_SECURE_PATTERN = re.compile(r'<meta property="og:audio:secure_url" content="https://esperanto12\.net/assets/ogg/01\.ogg" />')
OG_AUDIO_TYPE_PATTERN = re.compile(r'<meta property="og:audio:type" content="audio/ogg" />')
OG_AUDIO_ANY_PATTERN = re.compile(r'<meta property="og:audio"')
ROBOTS_SITEMAP_PATTERN = re.compile(r'Sitemap: https://esperanto12\.net/sitemap\.xml')
SITEMAP_EN_PATTERN = re.compile(r'<loc>https://esperanto12\.net/en/01/</loc>')
LLMS_ROOT_TITLE_PATTERN = re.compile(r'^# Esperanto12\.net$', re.M)
LLMS_ROOT_EN_PATTERN = re.compile(r'https://esperanto12\.net/en/llms\.txt\)')
LLMS_ROOT_DE_PATTERN = re.compile(r'https://esperanto12\.net/de/llms\.txt\)')
LLMS_ROOT_BE_PATTERN = re.compile(r'https://esperanto12\.net/be/llms\.txt\)')
LLMS_EN_FULL_PATTERN = re.compile(r'https://esperanto12\.net/en/llms-full\.txt\)')
LLMS_EN_LESSON_PATTERN = re.compile(r'https://esperanto12\.net/en/01/')
LLMS_EN_TABELVORTOJ_PATTERN = re.compile(r'https://esperanto12\.net/en/tabelvortoj/')
LLMS_EN_DUPLICATE_INTRO_PATTERN = re.compile(
    r'\(https://esperanto12\.net/en/\): Teaches the most important 500 words\.'
)
LLMS_FULL_LESSON_1_PATTERN = re.compile(r'Amiko\s+Marko')
LLMS_FULL_LESSON_12_PATTERN = re.compile(r'Nokta\s+promeno')
RAW_TEMPLATE_PATTERN = re.compile(r'\{\{[^}]+\}\}')
FONT_DISPLAY_OPTIONAL_PATTERN = re.compile(r'font-display:optional')
FONT_DISPLAY_SWAP_PATTERN = re.compile(r'font-display:\s*swap')


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


def require_lesson_image_alts(output_dir, lingvo):
    for leciono in range(1, 13):
        leciono_numero = str(leciono).zfill(2)
        path = output_dir / lingvo / leciono_numero / 'index.html'
        pattern = re.compile(
            rf'<img class="leciona" src="/{re.escape(lingvo)}/\.\./'
            rf'assets/img/lecionaj/{leciono_numero}\.webp" alt="[^"]+" />'
        )
        require_pattern(path, pattern)


def forbid_pattern(path, pattern):
    require_nonempty_file(path)
    try:
        text = path.read_text(encoding='utf-8')
    except UnicodeDecodeError as error:
        fail('ne eblas legi kiel UTF-8 ' + str(path) + ': ' + str(error))
    if pattern.search(text):
        fail('trovis neatenditan enhavon en ' + str(path))


def require_font_preloads(path, href_prefix):
    for subset, weight in (
        ('latin', 400),
        ('latin-ext', 400),
        ('latin', 700),
    ):
        pattern = re.compile(
            r'<link\s+rel="preload"\s+href="'
            + re.escape(href_prefix)
            + rf'assets/files/fira-sans-{subset}-{weight}-normal\.woff2"'
            + r'\s+as="font"\s+type="font/woff2"\s+crossorigin\s*/>',
            re.S,
        )
        require_pattern(path, pattern)


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
        output_dir / 'favicon-120x120.png',
        output_dir / 'favicon.ico',
        output_dir / 'apple-touch-icon.png',
        output_dir / 'robots.txt',
        output_dir / 'sitemap.xml',
        output_dir / 'llms.txt',
        lingvo_dir / 'index.html',
        lingvo_dir / 'llms.txt',
        lingvo_dir / 'llms-full.txt',
        output_dir / 'assets' / 'bundle.css',
        output_dir / 'assets' / 'bundle.js',
        output_dir / 'assets' / 'hejmo.js',
        output_dir / 'assets' / 'img' / 'logo' / 'logo-64.png',
        output_dir / 'assets' / 'img' / 'logo' / 'logo-256.png',
        output_dir / 'assets' / 'img' / 'logo' / 'favicon-120x120.png',
        output_dir / 'assets' / 'img' / 'logo' / 'favicon-16x16.png',
        output_dir / 'assets' / 'img' / 'logo' / 'favicon-32x32.png',
        output_dir / 'pwa' / 'images' / 'icon-192.png',
        output_dir / 'pwa' / 'images' / 'icon-512.png',
    ]:
        require_nonempty_file(path)

    require_pattern(output_dir / 'robots.txt', ROBOTS_SITEMAP_PATTERN)
    require_pattern(output_dir / 'sitemap.xml', SITEMAP_EN_PATTERN)
    require_pattern(output_dir / 'llms.txt', LLMS_ROOT_TITLE_PATTERN)
    require_pattern(output_dir / 'llms.txt', LLMS_ROOT_EN_PATTERN)
    require_pattern(output_dir / 'llms.txt', LLMS_ROOT_DE_PATTERN)
    forbid_pattern(output_dir / 'llms.txt', LLMS_ROOT_BE_PATTERN)
    require_pattern(lingvo_dir / 'llms.txt', LLMS_EN_FULL_PATTERN)
    require_pattern(lingvo_dir / 'llms.txt', LLMS_EN_LESSON_PATTERN)
    require_pattern(lingvo_dir / 'llms.txt', LLMS_EN_TABELVORTOJ_PATTERN)
    forbid_pattern(lingvo_dir / 'llms.txt', LLMS_EN_DUPLICATE_INTRO_PATTERN)
    require_pattern(lingvo_dir / 'llms-full.txt', LLMS_FULL_LESSON_1_PATTERN)
    require_pattern(lingvo_dir / 'llms-full.txt', LLMS_FULL_LESSON_12_PATTERN)
    forbid_pattern(lingvo_dir / 'llms-full.txt', RAW_TEMPLATE_PATTERN)
    require_pattern(lingvo_dir / 'index.html', HTML_LANG_PATTERN)
    require_pattern(lingvo_dir / 'index.html', TITLE_ROOT_PATTERN)
    require_pattern(lingvo_dir / 'index.html', META_DESCRIPTION_PATTERN)
    require_pattern(lingvo_dir / 'index.html', CANONICAL_ROOT_PATTERN)
    require_pattern(lingvo_dir / 'index.html', HREFLANG_EN_PATTERN)
    require_pattern(lingvo_dir / 'index.html', HREFLANG_DE_PATTERN)
    require_pattern(lingvo_dir / 'index.html', HREFLANG_X_DEFAULT_PATTERN)
    require_pattern(lingvo_dir / 'index.html', OG_URL_ROOT_PATTERN)
    require_pattern(lingvo_dir / 'index.html', OG_SITE_NAME_PATTERN)
    require_pattern(lingvo_dir / 'index.html', OG_DESCRIPTION_PATTERN)
    require_pattern(lingvo_dir / 'index.html', OG_LOCALE_EN_PATTERN)
    require_pattern(lingvo_dir / 'index.html', OG_LOCALE_ALTERNATE_DE_PATTERN)
    require_pattern(lingvo_dir / '01' / 'index.html', CANONICAL_LESSON_PATTERN)
    require_pattern(lingvo_dir / '01' / 'index.html', OG_URL_LESSON_PATTERN)
    require_pattern(lingvo_dir / '01' / 'index.html', OG_AUDIO_PATTERN)
    require_pattern(lingvo_dir / '01' / 'index.html', OG_AUDIO_SECURE_PATTERN)
    require_pattern(lingvo_dir / '01' / 'index.html', OG_AUDIO_TYPE_PATTERN)
    forbid_pattern(lingvo_dir / '01' / 'vortoj' / 'index.html', OG_AUDIO_ANY_PATTERN)
    require_pattern(lingvo_dir / '01' / 'index.html', META_DESCRIPTION_PATTERN)
    require_font_preloads(output_dir / 'index.html', '')
    require_font_preloads(lingvo_dir / 'index.html', '/' + lingvo + '/../')
    require_lesson_image_alts(output_dir, lingvo)
    bundle_css = output_dir / 'assets' / 'bundle.css'
    require_pattern(bundle_css, FONT_DISPLAY_OPTIONAL_PATTERN)
    forbid_pattern(bundle_css, FONT_DISPLAY_SWAP_PATTERN)
    # La vendaj bibliotekoj troviĝas nun en la kunmetita bundle.js; iliaj
    # versiaj banneroj restas, ĉar la vendaj dosieroj ne estas re-minigitaj.
    bundle_js = output_dir / 'assets' / 'bundle.js'
    require_pattern(bundle_js, BOOTSTRAP_PATTERN)
    require_pattern(bundle_js, JQUERY_PATTERN)
    require_pattern(bundle_js, TYPEAHEAD_PATTERN)
    gramatiko_path = lingvo_dir / '01' / 'gramatiko' / 'index.html'
    require_pattern(gramatiko_path, GRAMATIKO_PATTERN)
    require_pattern(gramatiko_path, GRAMATIKO_TOC_PATTERN)
    require_pattern(gramatiko_path, GRAMATIKO_EMFAZO_PATTERN)
    require_apkg(lingvo_dir / 'eksporto' / (lingvo + '.apkg'))

    print('Sukcesis: kontrolis Markdown-, HTML- kaj Anki-eligon por ' + lingvo)


if __name__ == '__main__':
    main()
