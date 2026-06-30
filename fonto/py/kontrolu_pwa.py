#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import re
from pathlib import Path

from . import pwa
from .generu import AGORDOJ_DIR, legi_yaml


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


def read_text_file(path):
    require_nonempty_file(path)
    try:
        return path.read_text(encoding='utf-8')
    except UnicodeDecodeError as error:
        fail('ne eblas legi kiel UTF-8 ' + str(path) + ': ' + str(error))


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


def check_manifest(output_dir, precache_urls):
    manifest_path = output_dir / 'manifest.webmanifest'
    require_nonempty_file(manifest_path)
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as error:
        fail('manifest.webmanifest ne estas valida JSON: ' + str(error))

    require(manifest.get('scope') == '/', 'manifest scope ne estas /')
    require(manifest.get('start_url') == '/', 'manifest start_url ne estas /')
    require(manifest.get('display') == 'standalone', 'manifest display ne estas standalone')
    icons = manifest.get('icons')
    require(isinstance(icons, list) and icons, 'manifest ne enhavas ikonojn')

    for icon in icons:
        src = icon.get('src')
        require(src and src.startswith('/'), 'ikono ne havas radikan src')
        icon_path = output_dir / src.lstrip('/')
        require_nonempty_file(icon_path)
        require(src in precache_urls, 'ikono mankas en precache: ' + src)


def check_precache_completeness(output_dir, precache_urls):
    expected_urls = set(pwa.collect_precache_urls(output_dir))
    missing = sorted(expected_urls - precache_urls)
    unexpected = sorted(precache_urls - expected_urls)
    if missing:
        fail('mankas ' + str(len(missing)) + ' dosieroj en precache, ekzemple: ' + ', '.join(missing[:10]))
    if unexpected:
        fail('precache enhavas nekonatajn URL-ojn, ekzemple: ' + ', '.join(unexpected[:10]))


def check_languages(output_dir, lingvoj, precache_urls):
    for lingvo in lingvoj:
        required_urls = [
            '/' + lingvo + '/index.html',
            '/' + lingvo + '/01/index.html',
            '/' + lingvo + '/01/gramatiko/index.html',
            '/' + lingvo + '/js/vortlisto.js',
            '/' + lingvo + '/eksporto/' + lingvo + '.apkg',
        ]
        for url in required_urls:
            require_nonempty_file(output_dir / url.lstrip('/'))
            require(url in precache_urls, 'mankas lingva URL en precache: ' + url)


def check_seo(output_dir, lingvoj, precache_urls):
    robots_path = output_dir / 'robots.txt'
    sitemap_path = output_dir / 'sitemap.xml'
    require_nonempty_file(robots_path)
    require_nonempty_file(sitemap_path)
    require('/robots.txt' in precache_urls, 'robots.txt mankas en precache')
    require('/sitemap.xml' in precache_urls, 'sitemap.xml mankas en precache')

    robots_text = read_text_file(robots_path)
    sitemap_text = read_text_file(sitemap_path)
    require('User-agent: *' in robots_text, 'robots.txt ne enhavas User-agent')
    require('Allow: /' in robots_text, 'robots.txt ne permesas /')
    require(
        'Sitemap: https://esperanto12.net/sitemap.xml' in robots_text,
        'robots.txt ne ligas al la sitemap',
    )

    lingvaj_agordoj = legi_yaml(AGORDOJ_DIR / 'lingvoj.yml')
    pretaj_lingvoj = [
        lingvo
        for lingvo in lingvoj
        if lingvaj_agordoj.get(lingvo, {}).get('stato') == 'preta'
    ]
    testaj_lingvoj = [
        lingvo
        for lingvo in lingvoj
        if lingvaj_agordoj.get(lingvo, {}).get('stato') == 'testa'
    ]

    require(
        'https://esperanto12.net/en/01/' in sitemap_text,
        'sitemap ne enhavas pretan anglan lecionon',
    )
    for lingvo in pretaj_lingvoj:
        require(
            f'https://esperanto12.net/{lingvo}/' in sitemap_text,
            'preta lingvo mankas en sitemap: ' + lingvo,
        )

    angla_indekso = read_text_file(output_dir / 'en' / 'index.html')
    for lingvo in testaj_lingvoj:
        test_url = f'https://esperanto12.net/{lingvo}/'
        require(test_url not in sitemap_text, 'testa lingvo aperas en sitemap: ' + lingvo)
        require(
            f'hreflang="{lingvo}"' not in angla_indekso,
            'testa lingvo aperas en hreflang de angla pagxo: ' + lingvo,
        )

        test_page = output_dir / lingvo / 'index.html'
        if test_page.is_file():
            test_text = read_text_file(test_page)
            require(
                '<meta name="robots" content="noindex, follow" />' in test_text,
                'testa lingvo ne havas noindex: ' + lingvo,
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--lingvoj', nargs='+', required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    service_worker_path = output_dir / 'sw.js'
    require_nonempty_file(service_worker_path)
    require_nonempty_file(output_dir / 'pwa' / 'registru.js')

    precache_urls, service_worker_text = load_precache_urls(service_worker_path)
    require('CACHE_NAME' in service_worker_text, 'mankas CACHE_NAME en service worker')
    require('/manifest.webmanifest' in precache_urls, 'manifest mankas en precache')
    require('/pwa/registru.js' in precache_urls, 'registrilo mankas en precache')

    check_manifest(output_dir, precache_urls)
    check_languages(output_dir, args.lingvoj, precache_urls)
    check_seo(output_dir, args.lingvoj, precache_urls)
    check_precache_completeness(output_dir, precache_urls)

    print('Sukcesis: kontrolis PWA-on kaj offline-liston por ' + str(len(args.lingvoj)) + ' lingvoj')


if __name__ == '__main__':
    main()
