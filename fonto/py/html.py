#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET

import genanki
import jinja2
from markupsafe import Markup
import mistune

from .ankroj import forigu_html, unika_ankro
from . import md as md_generilo
from . import pwa


ROOT_DIR = Path(__file__).resolve().parents[2]
FONTO_DIR = ROOT_DIR / 'fonto'
NODE_MODULES_DIR = ROOT_DIR / 'node_modules'
AKTIVOJ_DIST_DIR = FONTO_DIR / 'aktivoj' / 'dist'
OUTPUT_DIR = ROOT_DIR / 'eligo' / 'retejo'
SITE_URL = 'https://esperanto12.net'
GITHUB_CONTENT_BASE = 'https://github.com/Esperanto/kurso-zagreba-metodo'
SITEMAP_NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
ALDONAJ_PAGXOJ = ('tabelvortoj', 'prepozicioj', 'konjunkcioj', 'afiksoj', 'diversajxoj', 'auxtoroj', 'post')
LECIONAJ_TAB_VOJOJ = ('', 'vortoj/', 'gramatiko/', 'ekzerco1/', 'ekzerco2/', 'ekzerco3/')
LLMS_FULL_PRINTENDAJ = {
    'partoj': (
        'teksto',
        'vortoj',
        'gramatiko',
        'ekzerco1',
        'ekzerco2',
        'ekzerco3',
        'solvo1',
        'solvo2',
        'solvo3',
    ),
    'lecionoj': tuple(range(1, 13)),
}

ET.register_namespace('', SITEMAP_NS)


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


class AnkrohavaHTMLRenderer(mistune.HTMLRenderer):
    def __init__(self):
        super().__init__()
        self._uzitaj_ankroj = {}

    def heading(self, text, level, **attrs):
        ankro = unika_ankro(forigu_html(text), self._uzitaj_ankroj)
        return '<h{level} id="{ankro}">{text}</h{level}>\n'.format(
            ankro=mistune.escape(ankro),
            level=level,
            text=text,
        )

    def link(self, text, url, title=None):
        title_attr = ''
        if title:
            title_attr = ' title="{}"'.format(mistune.escape(title))
        target_attr = ''
        if url.startswith(('http://', 'https://')):
            target_attr = ' target="_blank" rel="noopener"'
        return '<a href="{}"{}{}>{}</a>'.format(
            mistune.escape_url(url),
            title_attr,
            target_attr,
            text,
        )


def render_markdown(text):
    md = mistune.create_markdown(
        renderer=AnkrohavaHTMLRenderer(),
        plugins=[morfema_emfazo],
    )
    return Markup(md(text))


def normaligu_spacojn(text):
    return re.sub(r'\s+', ' ', text).strip()


def markdown_link(label, url, description=None):
    label = str(label).replace('[', '\\[').replace(']', '\\]')
    line = f'- [{label}]({url})'
    if description:
        line += ': ' + normaligu_spacojn(str(description))
    return line


def meta_description_from_markdown(text):
    text = re.sub(r'\{\{\s*url\.[^}]+\s*\}\}', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)

    partoj = []
    alineo = []

    def finu_alineon():
        if alineo:
            partoj.append(' '.join(alineo))
            alineo.clear()

    for linio in text.splitlines():
        linio = linio.strip()
        if not linio or re.fullmatch(r'[-_*]{3,}', linio):
            finu_alineon()
            continue

        listero = re.match(r'^[-+]\s+(.*)$', linio)
        if listero:
            finu_alineon()
            partoj.append(listero.group(1))
            continue

        alineo.append(linio)

    finu_alineon()

    purigitaj_partoj = []
    for parto in partoj:
        parto = re.sub(r'[*_`#>]', '', parto)
        parto = re.sub(r'\s+', ' ', parto).strip()
        if parto:
            purigitaj_partoj.append(parto)

    priskribo = ''
    for parto in purigitaj_partoj:
        if not priskribo:
            priskribo = parto
            continue
        if priskribo[-1] in '.!?…؟。！？':
            priskribo += ' ' + parto
        else:
            priskribo += '. ' + parto

    return priskribo


def og_bildo_url(lingvo):
    lingva_bildo = FONTO_DIR / 'bildoj' / 'og' / f'{lingvo}.png'
    if lingva_bildo.is_file():
        return f'{SITE_URL}/assets/img/og/{lingvo}.png'
    return f'{SITE_URL}/assets/img/og.png'


def absoluta_url(vojo):
    if not vojo.startswith('/'):
        vojo = '/' + vojo
    return SITE_URL + vojo


def pretaj_lingvokodoj(lingvoj):
    return [
        kodo
        for kodo, lingvo in sorted(lingvoj.items())
        if lingvo.get('stato') == 'preta'
    ]


def normaligu_relativan_vojon(relativa_vojo):
    if not relativa_vojo:
        return ''
    relativa_vojo = relativa_vojo.lstrip('/')
    if not relativa_vojo.endswith('/'):
        relativa_vojo += '/'
    return relativa_vojo


def lingva_vojo(lingvo, relativa_vojo=''):
    relativa_vojo = normaligu_relativan_vojon(relativa_vojo)
    return '/' + lingvo + '/' + relativa_vojo


def lingva_dosiero_url(lingvo, relativa_vojo):
    return absoluta_url('/' + lingvo + '/' + relativa_vojo.lstrip('/'))


def alternaj_ligiloj(lingvoj, relativa_vojo, inkluzivu_x_default=True):
    alternaj = [
        {
            'hreflang': kodo,
            'url': absoluta_url(lingva_vojo(kodo, relativa_vojo)),
        }
        for kodo in pretaj_lingvokodoj(lingvoj)
    ]
    if inkluzivu_x_default:
        alternaj.append({
            'hreflang': 'x-default',
            'url': absoluta_url('/'),
        })
    return alternaj


def seo_datenoj(enhavo, relativa_vojo=''):
    lingvo = enhavo['lingvo']
    stato = enhavo['lingvoj'][lingvo].get('stato')
    alternaj = []
    if stato == 'preta':
        alternaj = alternaj_ligiloj(enhavo['lingvoj'], relativa_vojo)

    return {
        'canonical_url': absoluta_url(lingva_vojo(lingvo, relativa_vojo)),
        'alternaj_ligiloj': alternaj,
        'meta_description': meta_description_from_markdown(enhavo['enkonduko']),
        'noindex': stato == 'testa',
    }


def hejma_seo_datenoj(hejmaj_lingvoj):
    lingvokodoj = sorted(lingvo['kodo'] for lingvo in hejmaj_lingvoj)
    alternaj = [
        {
            'hreflang': kodo,
            'url': absoluta_url('/' + kodo + '/'),
        }
        for kodo in lingvokodoj
    ]
    alternaj.append({
        'hreflang': 'x-default',
        'url': absoluta_url('/'),
    })

    return {
        'canonical_url': absoluta_url('/'),
        'alternaj_ligiloj': alternaj,
        'noindex': False,
    }


def sitemap_relativaj_vojoj():
    yield ''
    for pagxo in ALDONAJ_PAGXOJ:
        yield pagxo + '/'
    for i in range(1, 13):
        i_padded = str(i).zfill(2)
        for tab_vojo in LECIONAJ_TAB_VOJOJ:
            yield i_padded + '/' + tab_vojo


def aldonu_sitemap_url(urlset, loc):
    url = ET.SubElement(urlset, ET.QName(SITEMAP_NS, 'url'))
    ET.SubElement(url, ET.QName(SITEMAP_NS, 'loc')).text = loc


def render_sitemap(lingvoj, generitaj_lingvoj):
    sitemap_lingvoj = [
        kodo
        for kodo in sorted(generitaj_lingvoj)
        if lingvoj[kodo].get('stato') == 'preta'
    ]
    urlset = ET.Element(ET.QName(SITEMAP_NS, 'urlset'))

    aldonu_sitemap_url(urlset, absoluta_url('/'))

    for relativa_vojo in sitemap_relativaj_vojoj():
        for lingvo in sitemap_lingvoj:
            aldonu_sitemap_url(
                urlset,
                absoluta_url(lingva_vojo(lingvo, relativa_vojo)),
            )

    return ET.tostring(urlset, encoding='unicode', xml_declaration=True)


def generate_seo_files(lingvoj, generitaj_lingvoj):
    write_file(
        OUTPUT_DIR / 'robots.txt',
        'User-agent: *\n'
        'Allow: /\n'
        'Sitemap: ' + absoluta_url('/sitemap.xml') + '\n',
    )
    write_file(
        OUTPUT_DIR / 'sitemap.xml',
        render_sitemap(lingvoj, generitaj_lingvoj),
    )


def kursa_titolo(enhavo):
    return (
        enhavo['fasado'].get('Lerni Esperanton')
        or enhavo['fasado'].get('Lerni Esperanton en 12 lecionoj')
        or 'Lerni Esperanton'
    )


def fasada_etikedo(enhavo, klavo):
    return enhavo['fasado'].get(klavo) or klavo


def render_llms_index(hejmaj_lingvoj, meta_description):
    lines = [
        '# Esperanto12.net',
        '',
        '> Esperanto12.net is a free Esperanto basics course using the Zagreb method. '
        + normaligu_spacojn(meta_description),
        '',
        '## Languages',
    ]
    for lingvo in hejmaj_lingvoj:
        lines.append(markdown_link(
            lingvo['nomo'],
            lingva_dosiero_url(lingvo['kodo'], 'llms.txt'),
            lingvo['titolo'],
        ))
    lines.extend([
        '',
        '## Resources',
        markdown_link(
            'Sitemap',
            absoluta_url('/sitemap.xml'),
            'XML sitemap for indexable pages.',
        ),
        '',
    ])
    return '\n'.join(lines)


def render_lingva_llms(enhavo, enkonduko):
    lingvo = enhavo['lingvo']
    priskribo = meta_description_from_markdown(enkonduko)
    lines = [
        '# ' + kursa_titolo(enhavo),
        '',
        '> ' + priskribo,
        '',
        '## ' + fasada_etikedo(enhavo, 'Lecionoj'),
        markdown_link(
            fasada_etikedo(enhavo, 'Lerni Esperanton en 12 lecionoj'),
            absoluta_url(lingva_vojo(lingvo)),
        ),
        markdown_link(
            '01. ' + enhavo['lecionoj'][0]['teksto']['titolo_string'],
            absoluta_url(lingva_vojo(lingvo, '01/')),
            fasada_etikedo(enhavo, 'Teksto'),
        ),
        markdown_link(
            fasada_etikedo(enhavo, 'Tabelvortoj'),
            absoluta_url(lingva_vojo(lingvo, 'tabelvortoj/')),
        ),
        markdown_link(
            fasada_etikedo(enhavo, 'Prepozicioj'),
            absoluta_url(lingva_vojo(lingvo, 'prepozicioj/')),
        ),
        markdown_link(
            fasada_etikedo(enhavo, 'Konjunkcioj'),
            absoluta_url(lingva_vojo(lingvo, 'konjunkcioj/')),
        ),
        markdown_link(
            fasada_etikedo(enhavo, 'Afiksoj'),
            absoluta_url(lingva_vojo(lingvo, 'afiksoj/')),
        ),
        markdown_link(
            fasada_etikedo(enhavo, 'Diversaĵoj'),
            absoluta_url(lingva_vojo(lingvo, 'diversajxoj/')),
        ),
        markdown_link(
            fasada_etikedo(enhavo, 'Trovu Esperanto-parolantojn'),
            absoluta_url(lingva_vojo(lingvo, 'post/')),
        ),
        '',
        '## llms-full.txt',
        markdown_link(
            'llms-full.txt',
            lingva_dosiero_url(lingvo, 'llms-full.txt'),
        ),
        '',
        '## Optional',
        markdown_link(
            'Sitemap',
            absoluta_url('/sitemap.xml'),
        ),
        '',
    ]
    return '\n'.join(lines)


def render_lingva_llms_full(enhavo, enkonduko):
    enhavo_md = dict(enhavo)
    enhavo_md['enkonduko'] = enkonduko
    return md_generilo.rendu_md(
        enhavo_md,
        LLMS_FULL_PRINTENDAJ,
        template='llms-full.md',
        llms=True,
    )


def render_page(name, enhavo, vojprefikso, env, redaktaj_ligiloj=None):
    rendered = env.get_template(name + '.html').render(
        enhavo=enhavo,
        vojprefikso=vojprefikso,
        redaktaj_ligiloj=redaktaj_ligiloj or [],
        seo=seo_datenoj(enhavo, name + '/'),
    )

    return rendered


def github_content_url(lingvo, path, kind='blob'):
    return f'{GITHUB_CONTENT_BASE}/{kind}/master/enhavo/tradukenda/{lingvo}/{path}'


def redaktaj_ligiloj(lingvo, tab=None, leciono=None):
    if tab is None:
        return [
            {
                'teksto': 'Redaktu tiun ĉi enhavon',
                'url': github_content_url(lingvo, 'enkonduko.md'),
            }
        ]

    if tab in ('teksto', 'vortoj'):
        return [
            {
                'teksto': 'Redaktu tiun ĉi enhavon',
                'url': github_content_url(lingvo, 'vortaro', 'tree'),
            }
        ]

    if tab == 'gramatiko':
        return [
            {
                'teksto': 'Redaktu tiun ĉi enhavon',
                'url': github_content_url(lingvo, f'gramatiko/{leciono}.md'),
            }
        ]

    if tab == 'ekzerco1':
        return [
            {
                'teksto': 'Redaktu tiun ĉi enhavon',
                'url': github_content_url(lingvo, f'ekzercoj/traduku/{leciono}.yml'),
            }
        ]

    if tab == 'ekzerco3':
        return [
            {
                'teksto': 'Redaktu tiun ĉi enhavon',
                'url': github_content_url(lingvo, f'ekzercoj/traduku-kaj-respondu/{leciono}.yml'),
            },
        ]

    if tab == 'post':
        return [
            {
                'teksto': 'Redaktu tiun ĉi enhavon',
                'url': github_content_url(lingvo, 'post.md'),
            }
        ]

    if tab == 'tabelvortoj':
        return [
            {
                'teksto': 'Redaktu tiun ĉi enhavon',
                'url': github_content_url(lingvo, 'vortaro/tabelvorto.yml'),
            }
        ]

    if tab == 'prepozicioj':
        return [
            {
                'teksto': 'Redaktu tiun ĉi enhavon',
                'url': github_content_url(lingvo, 'vortaro/prepozicio.yml'),
            }
        ]

    if tab == 'konjunkcioj':
        return [
            {
                'teksto': 'Redaktu tiun ĉi enhavon',
                'url': github_content_url(lingvo, 'vortaro/konjunkcio.yml'),
            }
        ]

    if tab == 'afiksoj':
        return [
            {
                'teksto': 'Redaktu prefiksojn',
                'url': github_content_url(lingvo, 'vortaro/prefikso.yml'),
            },
            {
                'teksto': 'Redaktu sufiksojn',
                'url': github_content_url(lingvo, 'vortaro/sufikso.yml'),
            },
        ]

    if tab == 'diversajxoj':
        return [
            {
                'teksto': 'Redaktu tiun ĉi enhavon',
                'url': github_content_url(lingvo, 'vortaro', 'tree'),
            }
        ]

    return []


def write_file(filename, content):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


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


def render_hejmo(versio, meta_description, hejmaj_lingvoj):
    env = jinja2.Environment(auto_reload=False)
    env.loader = jinja2.FileSystemLoader(str(FONTO_DIR / 'html'))
    return env.get_template('hejmo.html').render(
        hejmaj_lingvoj=hejmaj_lingvoj,
        meta_description=meta_description,
        seo=hejma_seo_datenoj(hejmaj_lingvoj),
        site_url=SITE_URL,
        versio=versio,
    )


def copy_static_files(versio, meta_description, hejmaj_lingvoj):
    static_dirs = [
        (FONTO_DIR / 'sonoj' / 'mp3', OUTPUT_DIR / 'assets' / 'mp3'),
        (FONTO_DIR / 'sonoj' / 'ogg', OUTPUT_DIR / 'assets' / 'ogg'),
    ]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_file(
        str(OUTPUT_DIR / 'index.html'),
        render_hejmo(versio, meta_description, hejmaj_lingvoj),
    )
    write_file(
        str(OUTPUT_DIR / 'llms.txt'),
        render_llms_index(hejmaj_lingvoj, meta_description),
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

    # Kopiu la esbuild-pakaĵojn (vd. fonto/aktivoj/bundlo.mjs).
    if not (AKTIVOJ_DIST_DIR / 'bundle.css').is_file():
        raise SystemExit('Mankas la pakaĵoj en ' + str(AKTIVOJ_DIST_DIR) + '. Rulu `make bundle`.')
    assets_dir = OUTPUT_DIR / 'assets'
    assets_dir.mkdir(parents=True, exist_ok=True)
    for nomo in ('bundle.css', 'bundle.js', 'hejmo.js'):
        shutil.copy2(AKTIVOJ_DIST_DIR / nomo, assets_dir / nomo)
    shutil.rmtree(assets_dir / 'files', ignore_errors=True)
    shutil.copytree(AKTIVOJ_DIST_DIR / 'files', assets_dir / 'files')


def generate_pwa():
    pwa.write_service_worker(OUTPUT_DIR, get_version_hash())


def generate_html(
    lingvo,
    enhavo,
    args,
    kopiu_statikan=True,
    hejmaj_lingvoj=None,
):
    eligo = {}
    versio = get_version_hash()
    enhavo['versio'] = versio
    enhavo['og_bildo_url'] = og_bildo_url(lingvo)
    if kopiu_statikan:
        angla_enkonduko = (ROOT_DIR / 'enhavo' / 'tradukenda' / 'en' / 'enkonduko.md').read_text(
            encoding='utf-8',
        )
        copy_static_files(
            versio,
            meta_description_from_markdown(angla_enkonduko),
            hejmaj_lingvoj or [],
        )

    env = jinja2.Environment(auto_reload=False)
    env.filters['markdown'] = render_markdown
    env.filters['normaligu_spacojn'] = normaligu_spacojn
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

    # La apendico aperas kiel «leciono 13» kun ĉi tiuj langetoj (flataj URL-oj).
    apendicaj_langetoj = [
        ('tabelvortoj', 'tabelvortoj/', enhavo['fasado']['Tabelvortoj']),
        ('prepozicioj', 'prepozicioj/', enhavo['fasado']['Prepozicioj']),
        ('konjunkcioj', 'konjunkcioj/', enhavo['fasado']['Konjunkcioj']),
        ('afiksoj', 'afiksoj/', enhavo['fasado']['Afiksoj']),
        ('diversajxoj', 'diversajxoj/', enhavo['fasado']['Diversaĵoj']),
    ]

    if args.vojprefikso:
        vojprefikso = args.vojprefikso + lingvo + '/'
    else:
        vojprefikso = '/' + lingvo + '/'

    url = {
        'anki': 'https://apps.ankiweb.net/',
        'kartaro': vojprefikso + 'eksporto/' + lingvo + '.apkg',
    }
    llms_url = {
        'anki': 'https://apps.ankiweb.net/',
        'kartaro': lingva_dosiero_url(lingvo, 'eksporto/' + lingvo + '.apkg'),
    }
    enkonduko = env.from_string(enhavo['enkonduko']).render(url=url)
    llms_enkonduko = env.from_string(enhavo['enkonduko']).render(url=llms_url)

    rendered = env.get_template('index.html').render(
        enhavo=enhavo,
        enkonduko=enkonduko,
        pretaj_lingvoj=[
            (kodo, lingvo)
            for kodo, lingvo in sorted(enhavo['lingvoj'].items())
            if lingvo.get('stato') == 'preta'
        ],
        url=url,
        vojprefikso=vojprefikso,
        redaktaj_ligiloj=redaktaj_ligiloj(lingvo),
        seo=seo_datenoj(enhavo),
        tabs=tabs,
    )

    eligo[output_path / 'index.html'] = rendered
    if enhavo['lingvoj'][lingvo].get('stato') == 'preta':
        eligo[output_path / 'llms.txt'] = render_lingva_llms(enhavo, llms_enkonduko)
        eligo[output_path / 'llms-full.txt'] = render_lingva_llms_full(enhavo, llms_enkonduko)

    # vortaro.js
    rendered = env.get_template('vortlisto.js').render(
        enhavo=enhavo,
    )
    eligo[output_path / 'js' / 'vortlisto.js'] = rendered

    eligo[output_path / 'eksporto' / (enhavo['lingvo'] + '.apkg')] = create_anki(enhavo)

    # Memstaraj aldonaj paĝoj (ne parto de la langetoj nek de la antaŭen/malantaŭen-fluo).
    for tab_page in ('auxtoroj', 'post'):
        pagxaj_ligiloj = redaktaj_ligiloj(lingvo, tab_page)
        eligo[output_path / tab_page / 'index.html'] = render_page(tab_page, enhavo, vojprefikso, env, pagxaj_ligiloj)

    # La fluo: 12 lecionoj × langetoj, poste la apendicaj langetoj kiel «leciono 13».
    paths = []
    for i in range(1, 13):
        for id, href, caption in tabs:
            paths.append(vojprefikso + str(i).zfill(2) + '/' + href)
    for id, href, caption in apendicaj_langetoj:
        paths.append(vojprefikso + href)

    paths_index = 0

    for i in range(1, 13):
        i_padded = str(i).zfill(2)
        leciono_dir = output_path / i_padded

        for tab, href, caption in tabs:

            previous_path = paths[paths_index - 1] if paths_index > 0 else None
            next_path = paths[paths_index + 1] if paths_index < len(paths) - 1 else None
            paths_index += 1

            tab_rendered = env.get_template(tab + '.html').render(
                enhavo=enhavo,
                leciono=enhavo['lecionoj'][i - 1],
                leciono_index=i,
                vojprefikso=vojprefikso,
                tab_vojprefikso=vojprefikso + i_padded + '/',
                previous_path=previous_path,
                next_path=next_path,
                tabs=tabs,
                active_tab=tab,
                identigilo=i_padded + '/' + href,
                redaktaj_ligiloj=redaktaj_ligiloj(lingvo, tab, i_padded),
                seo=seo_datenoj(enhavo, i_padded + '/' + href),
            )

            eligo[leciono_dir / href / 'index.html'] = tab_rendered

    # La apendico: samaj langetoj sur ĉiu paĝo, kaj daŭrigo de la sama fluo.
    for tab, href, caption in apendicaj_langetoj:

        previous_path = paths[paths_index - 1] if paths_index > 0 else None
        next_path = paths[paths_index + 1] if paths_index < len(paths) - 1 else None
        paths_index += 1

        apendica_rendered = env.get_template(tab + '.html').render(
            enhavo=enhavo,
            leciono_index=13,
            apendico=True,
            vojprefikso=vojprefikso,
            tab_vojprefikso=vojprefikso,
            previous_path=previous_path,
            next_path=next_path,
            tabs=apendicaj_langetoj,
            active_tab=tab,
            identigilo=href,
            redaktaj_ligiloj=redaktaj_ligiloj(lingvo, 'vortoj'),
            seo=seo_datenoj(enhavo, href),
        )

        eligo[output_path / tab / 'index.html'] = apendica_rendered

    # Forigu nunan dosierujon.
    shutil.rmtree(output_path, ignore_errors=True)

    # Kreu novajn dosierojn
    for vojo, eliga_enhavo in eligo.items():
        if vojo.suffix == '.apkg':
            vojo.parent.mkdir(parents=True, exist_ok=True)
            genanki.Package(eliga_enhavo).write_to_file(str(vojo))
            continue
        write_file(vojo, eliga_enhavo)
