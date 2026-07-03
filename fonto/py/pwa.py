#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import json
import shutil
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
FONTO_PWA_DIR = ROOT_DIR / 'fonto' / 'pwa'
FONTO_LOGO_DIR = ROOT_DIR / 'fonto' / 'bildoj' / 'logo'
CACHE_PREFIX = 'esperanto12'
PWA_THEME_COLOR = '#212529'
PWA_IMAGE_FILES = ('icon-192.png', 'icon-512.png')

# Komunaj (ne po-lingvaj) aktivoj, kiujn ĉiu lingva PWA bezonas por funkcii offline.
KOMUNAJ_AKTIVOJ = (
    'assets/bundle.css',
    'assets/bundle.js',
    'favicon.ico',
    'favicon-120x120.png',
    'apple-touch-icon.png',
)
KOMUNAJ_AKTIVAJ_DOSIERUJOJ = (
    'assets/files',   # tiparoj
    'assets/img',     # emblemoj, lecionaj bildoj ktp.
    'assets/ogg',     # sono (nur ogg, ne mp3)
    'pwa/images',     # PWA-ikonoj
)
# Ekster la offline-kaŝmemoro: og-bildoj estas nur por sociaj kraŭliloj.
EKSKLUZIVITAJ_PREFIKSOJ = ('assets/img/og',)


def copy_static_assets(output_dir):
    output_dir = Path(output_dir)
    images_dir = output_dir / 'pwa' / 'images'
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(images_dir, ignore_errors=True)
    images_dir.mkdir(parents=True, exist_ok=True)
    for image_file in PWA_IMAGE_FILES:
        shutil.copy2(FONTO_LOGO_DIR / image_file, images_dir / image_file)


def collect_precache_urls(output_dir, lingvo):
    output_dir = Path(output_dir)
    urls = []

    # Ĉiuj paĝoj kaj datenoj sub /{lingvo}/, krom la (granda) Anki-eksporto.
    lingvo_dir = output_dir / lingvo
    for path in sorted(lingvo_dir.rglob('*')):
        if not path.is_file():
            continue
        rel = path.relative_to(output_dir).as_posix()
        if rel.startswith('.') or path.name == 'sw.js':
            continue
        if path.suffix == '.apkg':
            continue
        urls.append('/' + rel)

    # Komunaj aktivoj, uzataj de la lingvaj paĝoj.
    for rel in KOMUNAJ_AKTIVOJ:
        if (output_dir / rel).is_file():
            urls.append('/' + rel)
    for subdir in KOMUNAJ_AKTIVAJ_DOSIERUJOJ:
        base = output_dir / subdir
        if not base.is_dir():
            continue
        for path in sorted(base.rglob('*')):
            if not path.is_file():
                continue
            rel = path.relative_to(output_dir).as_posix()
            if any(rel.startswith(prefikso) for prefikso in EKSKLUZIVITAJ_PREFIKSOJ):
                continue
            urls.append('/' + rel)

    return sorted(set(urls))


def app_name(lingvo):
    return 'Esperanto12 (' + lingvo + ')'


def render_manifest(lingvo, fasado):
    manifest = {
        'dir': 'auto',
        'lang': lingvo,
        'name': app_name(lingvo),
        'short_name': app_name(lingvo),
        'description': fasado['La plej rapida kurso por la bazoj'],
        'scope': '/' + lingvo + '/',
        'start_url': '/' + lingvo + '/',
        'display': 'standalone',
        'orientation': 'any',
        'theme_color': PWA_THEME_COLOR,
        'background_color': '#ffffff',
        'prefer_related_applications': False,
        'icons': [
            {'src': '/pwa/images/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
            {'src': '/pwa/images/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
        ],
    }
    return json.dumps(manifest, ensure_ascii=False, indent=2)


def fingerprint(output_dir, urls):
    output_dir = Path(output_dir)
    digest = hashlib.sha256()
    for url in urls:
        path = output_dir / url.lstrip('/')
        digest.update(url.encode('utf-8'))
        digest.update(b'\0')
        digest.update(path.read_bytes())
        digest.update(b'\0')
    return digest.hexdigest()[:12]


def write_service_worker(output_dir, lingvo, version):
    output_dir = Path(output_dir)
    urls = collect_precache_urls(output_dir, lingvo)
    prefix = CACHE_PREFIX + '-' + lingvo + '-'
    cache_name = prefix + version + '-' + fingerprint(output_dir, urls)
    precache_json = json.dumps(urls, ensure_ascii=False, indent=2)
    template = (FONTO_PWA_DIR / 'service-worker.js').read_text(encoding='utf-8')
    service_worker = (
        template
        .replace('__CACHE_NAME__', cache_name)
        .replace('__CACHE_PREFIX__', prefix)
        .replace('__OFFLINE_FALLBACK__', '/' + lingvo + '/index.html')
        .replace('__PRECACHE_URLS__', precache_json)
    )
    (output_dir / lingvo / 'sw.js').write_text(service_worker, encoding='utf-8')
    return urls
