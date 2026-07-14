#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import re
from pathlib import Path

from . import pwa


PRECACHE_PATTERN = re.compile(r'const PRECACHE_URLS = (\[.*?\]);', re.DOTALL)


def fail(message):
    raise SystemExit('PWA-kontrolo malsukcesis: ' + message)


def require(condition, message):
    if not condition:
        fail(message)


def require_nonempty_file(path):
    if not path.is_file():
        fail('mankas dosiero ' + str(path))
    if path.stat().st_size == 0:
        fail('malplenas dosiero ' + str(path))


def load_precache_urls(service_worker_path):
    text = service_worker_path.read_text(encoding='utf-8')
    match = PRECACHE_PATTERN.search(text)
    require(match, 'ne trovis PRECACHE_URLS en ' + str(service_worker_path))
    try:
        urls = json.loads(match.group(1))
    except json.JSONDecodeError as error:
        fail('PRECACHE_URLS ne estas valida JSON: ' + str(error))
    require(isinstance(urls, list), 'PRECACHE_URLS ne estas listo')
    return set(urls), text


def check_manifest(output_dir, lingvo, precache_urls):
    manifest_path = output_dir / lingvo / 'manifest.webmanifest'
    require_nonempty_file(manifest_path)
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as error:
        fail(str(manifest_path) + ' ne estas valida JSON: ' + str(error))

    scope = '/' + lingvo + '/'
    require(manifest.get('scope') == scope, 'manifest scope ne estas ' + scope)
    require(manifest.get('start_url') == scope, 'manifest start_url ne estas ' + scope)
    require(manifest.get('display') == 'standalone', 'manifest display ne estas standalone')
    require(manifest.get('name') == pwa.app_name(lingvo), 'manifest nomo ne estas ' + pwa.app_name(lingvo))
    require(manifest.get('short_name') == pwa.app_name(lingvo), 'manifest short_name ne estas ' + pwa.app_name(lingvo))
    require(manifest.get('theme_color') == pwa.PWA_THEME_COLOR, 'manifest theme_color estas malĝusta')
    icons = manifest.get('icons')
    require(isinstance(icons, list) and icons, 'manifest ne enhavas ikonojn')
    for icon in icons:
        src = icon.get('src')
        require(src and src.startswith('/'), 'ikono ne havas radikan src')
        require_nonempty_file(output_dir / src.lstrip('/'))
        require(src in precache_urls, 'ikono mankas en precache: ' + src)


def check_registration(output_dir, lingvo):
    index_path = output_dir / lingvo / 'index.html'
    require_nonempty_file(index_path)
    text = index_path.read_text(encoding='utf-8')
    require(
        'rel="manifest" href="/' + lingvo + '/manifest.webmanifest"' in text,
        'la starta paĝo ne ligas la manifeston: ' + lingvo,
    )
    require(
        "navigator.serviceWorker.register('/" + lingvo + "/sw.js')" in text,
        'la starta paĝo ne registras la service worker: ' + lingvo,
    )
    require(
        '<meta name="theme-color" content="' + pwa.PWA_THEME_COLOR + '" />' in text,
        'la starta paĝo ne havas ĝustan PWA-koloron: ' + lingvo,
    )
    require(
        "document.documentElement.classList.add('pwa-standalone')" in text,
        'la starta paĝo ne markas iOS-standalone-reĝimon: ' + lingvo,
    )
    require(
        'navbar-lingvoelektilo pwa-standalone-kasxita' in text,
        'la supra lingvoelektilo ne estas kaŝebla en PWA-kunteksto: ' + lingvo,
    )
    require(
        'lingva-startpagxo-lingvoelektilo pwa-standalone-kasxita' in text,
        'la startpaĝa lingvoelektilo ne estas kaŝebla en PWA-kunteksto: ' + lingvo,
    )
    require(
        'data-pwa-install' in text,
        'la startpaĝo ne havas PWA-instalbutonon: ' + lingvo,
    )
    require(
        'btn-outline-primary btn-lg pwa-install-butono pwa-standalone-kasxita' in text,
        'la PWA-instalbutono ne havas la atendatajn klasojn: ' + lingvo,
    )


def check_key_pages(output_dir, lingvo, precache_urls):
    required = [
        '/' + lingvo + '/index.html',
        '/' + lingvo + '/01/index.html',
        '/' + lingvo + '/01/gramatiko/index.html',
        '/' + lingvo + '/12/ekzerco3/index.html',
        '/' + lingvo + '/tabelvortoj/index.html',
        '/' + lingvo + '/js/vortlisto.js',
        '/' + lingvo + '/manifest.webmanifest',
        '/assets/bundle.css',
        '/assets/bundle.js',
    ]
    for url in required:
        require_nonempty_file(output_dir / url.lstrip('/'))
        require(url in precache_urls, 'mankas ŝlosila URL en precache: ' + url)

    # La granda Anki-eksporto NE estu en la offline-listo.
    apkg = '/' + lingvo + '/eksporto/' + lingvo + '.apkg'
    require(apkg not in precache_urls, 'la Anki-eksporto ne estu en precache: ' + apkg)


def check_pwa_state_bundle(output_dir):
    bundle_path = output_dir / 'assets' / 'bundle.js'
    require_nonempty_file(bundle_path)
    text = bundle_path.read_text(encoding='utf-8')
    require('esperanto12-pwa-state' in text, 'bundle.js ne enhavas la PWA-statan datumbazon')
    require('indexedDB' in text, 'bundle.js ne uzas IndexedDB por PWA-stato')
    require('display-mode: standalone' in text, 'bundle.js ne kontrolas standalone-reĝimon')
    require('pwa-standalone' in text, 'bundle.js ne enhavas iOS-standalone-fallbackon')
    require('input[data-solvo][id]' in text, 'bundle.js ne observas solveblajn enigkampojn')


def check_precache_completeness(output_dir, lingvo, precache_urls):
    expected = set(pwa.collect_precache_urls(output_dir, lingvo))
    missing = sorted(expected - precache_urls)
    unexpected = sorted(precache_urls - expected)
    if missing:
        fail('mankas ' + str(len(missing)) + ' dosieroj en precache, ekz.: ' + ', '.join(missing[:10]))
    if unexpected:
        fail('precache enhavas nekonatajn URL-ojn, ekz.: ' + ', '.join(unexpected[:10]))
    for url in precache_urls:
        require_nonempty_file(output_dir / url.lstrip('/'))


def check_language_pwa(output_dir, lingvo):
    sw_path = output_dir / lingvo / 'sw.js'
    require_nonempty_file(sw_path)
    precache_urls, sw_text = load_precache_urls(sw_path)
    require('CACHE_NAME' in sw_text, 'mankas CACHE_NAME en service worker: ' + lingvo)
    check_manifest(output_dir, lingvo, precache_urls)
    check_registration(output_dir, lingvo)
    check_key_pages(output_dir, lingvo, precache_urls)
    check_precache_completeness(output_dir, lingvo, precache_urls)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    # Ĉiu lingvo kun propra service worker havas instaleblan PWA-on.
    lingvoj = sorted(sw.parent.name for sw in output_dir.glob('*/sw.js'))
    require(lingvoj, 'neniu PWA-lingvo trovita en ' + str(output_dir))
    check_pwa_state_bundle(output_dir)
    for lingvo in lingvoj:
        check_language_pwa(output_dir, lingvo)

    print('Sukcesis: kontrolis la PWA-ojn por ' + str(len(lingvoj)) + ' lingvoj')


if __name__ == '__main__':
    main()
