#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import shutil
import subprocess

import genanki
import jinja2
from markupsafe import Markup
import mistune

from . import pwa


ROOT_DIR = Path(__file__).resolve().parents[2]
FONTO_DIR = ROOT_DIR / 'fonto'
NODE_MODULES_DIR = ROOT_DIR / 'node_modules'
OUTPUT_DIR = ROOT_DIR / 'eligo' / 'retejo'


def morfema_emfazo(md):
    def parse_morfema_emfazo(inline, match, state):
        child_state = state.copy()
        child_state.src = match.group('morfemo')
        state.append_token({
            'type': 'strong',
            'children': inline.render(child_state),
        })
        return match.end()

    md.inline.register(
        'morfema_emfazo',
        r'__(?P<morfemo>[^_\n]+?)__',
        parse_morfema_emfazo,
        before='emphasis',
    )


def render_page(name, enhavo, vojprefikso, env):
    rendered = env.get_template(name + '.html').render(
        enhavo=enhavo,
        vojprefikso=vojprefikso,
    )

    return rendered


def write_file(filename, content):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def copy_vendor_file(fonto, celo):
    if not fonto.is_file():
        raise SystemExit(
            'Mankas npm-vendordosiero ' + str(fonto) + '. Rulu `make install`.'
        )

    celo.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(fonto, celo)


def get_version_hash():
    github_sha = os.environ.get('GITHUB_SHA')
    if github_sha:
        return github_sha[:7]

    try:
        return subprocess.check_output(
            ['git', 'rev-parse', '--short=7', 'HEAD'],
            cwd=str(ROOT_DIR),
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return 'nekonata'


def aldonu_karton(deck, model, enhavo, radiko, leciono=None):
    # Ne kreu de tiuj vortspecoj.
    if enhavo['vortaro'][radiko]['vortspeco'] in ['interjekcio', 'nomo', 'vorto']:
        return deck

    esperanta_karto = radiko

    # Aldonu finaĵon.
    if radiko in enhavo['finajxoj']:
        esperanta_karto = esperanta_karto + enhavo['finajxoj'][radiko]

    # Aldonu '-' al afiksoj.
    if enhavo['vortaro'][radiko]['vortspeco'] in ['prefikso']:
        esperanta_karto = esperanta_karto + '-'
    if enhavo['vortaro'][radiko]['vortspeco'] in ['sufikso', 'finajxo']:
        esperanta_karto = '-' + esperanta_karto

    fontlingva_karto = enhavo['vortaro'][radiko]['tradukajxo']
    if isinstance(fontlingva_karto, list):
        fontlingva_karto = ', '.join(fontlingva_karto)

        # Ne kreu karton se iu de ili malplenas.
    if not esperanta_karto or not fontlingva_karto:
        return deck

    tags = [enhavo['vortaro'][radiko]['vortspeco'].replace(' ', '_')]
    if leciono:
        tags.append(leciono)

    note = genanki.Note(
        model=model,
        tags=tags,
        fields=[
            esperanta_karto,
            fontlingva_karto
        ]
    )
    deck.add_note(note)

    return deck


# Create an Anki file.
def create_anki(enhavo):
    model = genanki.Model(
        hash('Learn Esperanto') & ((1 << 31) - 1),
        'Learn Esperanto',
        fields=[
            {'name': 'eo'},
            {'name': enhavo['lingvo']},
        ],
        templates=[
            {
                'name': 'eo' + '-' + enhavo['lingvo'],
                'qfmt': '{{eo}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{' + enhavo['lingvo'] + '}}',
            },
            {
                'name': enhavo['lingvo'] + '-' + 'eo',
                'qfmt': '{{' + enhavo['lingvo'] + '}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{' + 'eo' + '}}',
            },
        ])

    deck = genanki.Deck(
        hash('Learn Esperanto: ' + enhavo['lingvo']) & ((1 << 31) - 1),
        'Learn Esperanto: ' + enhavo['lingvo']
    )

    aldonitaj = set()

    # Unue aldonu laux lecionoj.
    for leciono_index_0, leciono in enumerate(enhavo['lecionoj']):
        for radiko in leciono['vortoj']['teksto']:
            if radiko.lower() in enhavo['vortaro']:
                radiko = radiko.lower()
            leciono_numero = str(leciono_index_0 + 1)
            aldonu_karton(deck, model, enhavo, radiko, leciono_numero)
            aldonitaj.add(radiko)

    # Nun aldonu la reston.
    for radiko in enhavo['vortaro']:
        if radiko in aldonitaj:
            continue
        aldonu_karton(deck, model, enhavo, radiko)

    return deck


def render_cxefpagxo(versio, fasado, cxefpagxaj_lingvoj):
    env = jinja2.Environment(auto_reload=False)
    env.loader = jinja2.FileSystemLoader(str(FONTO_DIR / 'html'))
    return env.get_template('cxefpagxo.html').render(
        cxefpagxaj_lingvoj=cxefpagxaj_lingvoj,
        fasado=fasado,
        versio=versio,
    )


def copy_static_files(versio, cxefpagxa_fasado, cxefpagxaj_lingvoj):
    static_dirs = [
        (FONTO_DIR / 'css', OUTPUT_DIR / 'assets' / 'css'),
        (FONTO_DIR / 'js', OUTPUT_DIR / 'assets' / 'js'),
        (FONTO_DIR / 'sonoj' / 'mp3', OUTPUT_DIR / 'assets' / 'mp3'),
        (FONTO_DIR / 'sonoj' / 'ogg', OUTPUT_DIR / 'assets' / 'ogg'),
    ]
    vendor_files = [
        (
            NODE_MODULES_DIR / 'bootstrap' / 'dist' / 'css' / 'bootstrap.min.css',
            OUTPUT_DIR / 'vendor' / 'bootstrap' / 'css' / 'bootstrap.min.css',
        ),
        (
            NODE_MODULES_DIR / 'bootstrap' / 'dist' / 'js' / 'bootstrap.bundle.min.js',
            OUTPUT_DIR / 'vendor' / 'bootstrap' / 'js' / 'bootstrap.bundle.min.js',
        ),
        (
            NODE_MODULES_DIR / 'jquery' / 'dist' / 'jquery.min.js',
            OUTPUT_DIR / 'vendor' / 'jquery' / 'jquery.min.js',
        ),
        (
            NODE_MODULES_DIR / 'jquery-ui-dist' / 'jquery-ui.min.js',
            OUTPUT_DIR / 'vendor' / 'jquery' / 'jquery-ui.min.js',
        ),
        (
            NODE_MODULES_DIR / 'typeahead.js' / 'dist' / 'typeahead.bundle.min.js',
            OUTPUT_DIR / 'vendor' / 'typeahead' / 'typeahead.bundle.min.js',
        ),
    ]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_file(
        str(OUTPUT_DIR / 'index.html'),
        render_cxefpagxo(versio, cxefpagxa_fasado, cxefpagxaj_lingvoj),
    )
    shutil.copy2(FONTO_DIR / 'bildoj' / 'logo' / 'favicon.ico', OUTPUT_DIR / 'favicon.ico')
    shutil.copy2(FONTO_DIR / 'bildoj' / 'logo' / 'apple-touch-icon.png', OUTPUT_DIR / 'apple-touch-icon.png')
    pwa.copy_static_assets(OUTPUT_DIR)

    for fonto, celo in static_dirs:
        shutil.rmtree(celo, ignore_errors=True)
        shutil.copytree(fonto, celo)

    shutil.rmtree(OUTPUT_DIR / 'assets' / 'img', ignore_errors=True)
    shutil.copytree(
        FONTO_DIR / 'bildoj',
        OUTPUT_DIR / 'assets' / 'img',
        ignore=shutil.ignore_patterns('icon-192.png', 'icon-512.png'),
    )

    shutil.rmtree(OUTPUT_DIR / 'vendor', ignore_errors=True)
    for fonto, celo in vendor_files:
        copy_vendor_file(fonto, celo)

    fira_fonto = NODE_MODULES_DIR / '@fontsource' / 'fira-sans'
    fira_celo = OUTPUT_DIR / 'vendor' / 'fira-sans'
    if not fira_fonto.is_dir():
        raise SystemExit('Mankas @fontsource/fira-sans. Rulu `make install`.')
    fira_celo.mkdir(parents=True, exist_ok=True)
    for pezo in ('400', '700'):
        shutil.copy2(fira_fonto / f'{pezo}.css', fira_celo / f'{pezo}.css')
    (fira_celo / 'files').mkdir(parents=True, exist_ok=True)
    for f in (fira_fonto / 'files').glob('fira-sans-*-[47]00-normal.*'):
        shutil.copy2(f, fira_celo / 'files' / f.name)


def generate_pwa():
    pwa.write_service_worker(OUTPUT_DIR, get_version_hash())


def generate_html(
    lingvo,
    enhavo,
    args,
    kopiu_statikan=True,
    cxefpagxa_fasado=None,
    cxefpagxaj_lingvoj=None,
):
    eligo = {}
    md = mistune.create_markdown(plugins=[morfema_emfazo])
    versio = get_version_hash()
    enhavo['versio'] = versio
    if kopiu_statikan:
        copy_static_files(
            versio,
            cxefpagxa_fasado or enhavo['fasado'],
            cxefpagxaj_lingvoj or [],
        )

    env = jinja2.Environment(auto_reload=False)
    env.filters['markdown'] = lambda text: Markup(md(text))
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.loader = jinja2.FileSystemLoader(str(FONTO_DIR / 'html'))

    output_path = OUTPUT_DIR / lingvo

    tabs = [
        ('teksto', '', enhavo['fasado']['Teksto']),
        ('vortoj', 'vortoj/', enhavo['fasado']['Novaj vortoj']),
        ('gramatiko', 'gramatiko/', enhavo['fasado']['Gramatiko']),
        ('ekzerco1', 'ekzerco1/', enhavo['fasado']['Ekzerco 1']),
        ('ekzerco2', 'ekzerco2/', enhavo['fasado']['Ekzerco 2']),
        ('ekzerco3', 'ekzerco3/', enhavo['fasado']['Ekzerco 3'])
    ]

    if args.vojprefikso:
        vojprefikso = args.vojprefikso + lingvo + '/'
    else:
        vojprefikso = '/' + lingvo + '/'

    rendered = env.get_template('index.html').render(
        enhavo=enhavo,
        vojprefikso=vojprefikso,
        tabs=tabs,
    )

    eligo[output_path / 'index.html'] = rendered

    # vortaro.js
    rendered = env.get_template('vortlisto.js').render(
        enhavo=enhavo,
    )
    eligo[output_path / 'js' / 'vortlisto.js'] = rendered

    eligo[output_path / 'eksporto' / (enhavo['lingvo'] + '.apkg')] = create_anki(enhavo)

    for tab_page in ['tabelvortoj', 'prepozicioj', 'konjunkcioj', 'afiksoj', 'diversajxoj', 'auxtoroj', 'post']:
        eligo[output_path / tab_page / 'index.html'] = render_page(tab_page, enhavo, vojprefikso, env)

    paths = []
    for i in range(1, 13):
        for id, href, caption in tabs:
            paths.append(vojprefikso + str(i).zfill(2) + '/' + href)

    paths_index = 0

    for i in range(1, 13):
        i_padded = str(i).zfill(2)
        leciono_dir = output_path / i_padded

        for tab, href, caption in tabs:

            previous_path = None
            next_path = None

            tab_vojprefikso = vojprefikso + i_padded + '/'

            if paths_index > 0:
                previous_path = paths[paths_index - 1]
            if paths_index < len(paths) - 1:
                next_path = paths[paths_index + 1]
            paths_index += 1

            tab_rendered = env.get_template(tab + '.html').render(
                enhavo=enhavo,
                leciono=enhavo['lecionoj'][i - 1],
                leciono_index=i,
                vojprefikso=vojprefikso,
                tab_vojprefikso=tab_vojprefikso,
                previous_path=previous_path,
                next_path=next_path,
                tabs=tabs,
                active_tab=tab,
                identigilo=i_padded + '/' + href
            )

            eligo[leciono_dir / href / 'index.html'] = tab_rendered

    # Forigu nunan dosierujon.
    shutil.rmtree(output_path, ignore_errors=True)

    # Kreu novajn dosierojn
    for vojo, eliga_enhavo in eligo.items():
        if vojo.suffix == '.apkg':
            vojo.parent.mkdir(parents=True, exist_ok=True)
            genanki.Package(eliga_enhavo).write_to_file(str(vojo))
            continue
        write_file(vojo, eliga_enhavo)
