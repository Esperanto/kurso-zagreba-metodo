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
IGNORITAJ_DOSIEROJ = {'CNAME', 'sw.js'}
PWA_IMAGE_FILES = ('icon-192.png', 'icon-512.png')


def copy_static_assets(output_dir):
    output_dir = Path(output_dir)
    pwa_dir = output_dir / 'pwa'
    images_dir = pwa_dir / 'images'

    output_dir.mkdir(parents=True, exist_ok=True)
    pwa_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(FONTO_PWA_DIR / 'manifest.json', output_dir / 'manifest.webmanifest')
    shutil.copy2(FONTO_PWA_DIR / 'manifest.json', output_dir / 'manifest.json')
    shutil.copy2(FONTO_PWA_DIR / 'registru.js', pwa_dir / 'registru.js')

    shutil.rmtree(images_dir, ignore_errors=True)
    images_dir.mkdir(parents=True, exist_ok=True)
    for image_file in PWA_IMAGE_FILES:
        shutil.copy2(FONTO_LOGO_DIR / image_file, images_dir / image_file)


def collect_precache_urls(output_dir):
    output_dir = Path(output_dir)
    urls = []
    for path in sorted(output_dir.rglob('*')):
        if not path.is_file():
            continue

        relative_path = path.relative_to(output_dir)
        relative_name = relative_path.as_posix()
        if relative_name in IGNORITAJ_DOSIEROJ:
            continue
        if relative_name.startswith('.'):
            continue

        urls.append('/' + relative_name)

    return urls


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


def write_service_worker(output_dir, version):
    output_dir = Path(output_dir)
    urls = collect_precache_urls(output_dir)
    cache_name = CACHE_PREFIX + '-' + version + '-' + fingerprint(output_dir, urls)
    precache_json = json.dumps(urls, ensure_ascii=False, indent=2)
    template = (FONTO_PWA_DIR / 'service-worker.js').read_text(encoding='utf-8')
    service_worker = (
        template
        .replace('__CACHE_NAME__', cache_name)
        .replace('__PRECACHE_URLS__', precache_json)
    )
    (output_dir / 'sw.js').write_text(service_worker, encoding='utf-8')
    return urls
