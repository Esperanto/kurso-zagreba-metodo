#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import re
import argparse
from pathlib import Path

from . import html as html_generilo
from . import md as md_generilo
from .ankroj import forigu_html, unika_ankro


ROOT_DIR = Path(__file__).resolve().parents[2]
AGORDOJ_DIR = ROOT_DIR / 'agordoj'
ENHAVO_DIR = ROOT_DIR / 'enhavo'
LECION_NUMEROJ = range(1, 13)
YAML_LOADER = getattr(yaml, 'CSafeLoader', yaml.SafeLoader)
HTML_LINGVO_STATOJ = {'preta', 'testa'}
CXEFPAGXO_TITOLO = 'Lerni Esperanton'
CXEFPAGXO_SUBTITOLO = 'La plej rapida kurso por la bazoj'


class Fasado(dict):
    def __missing__(self, key):
        return key


def legi_yaml(path):
    with Path(path).open(encoding='utf-8-sig') as dosiero:
        return yaml.load(dosiero, Loader=YAML_LOADER)


def legi_tekston(path):
    return Path(path).read_text(encoding='utf-8-sig')


def transpose_headlines(markdown, level):
    prefix = '#' * level
    return re.sub(r'(^|\n)(#+)', lambda match: match.group(1) + prefix + match.group(2), markdown)


INTERPUNKCIO = set('.,;:!?«»“”„"\'()[]…')


def disigi_interpunkcion(segmentoj):
    """Apartigu komencan/finan interpunkcion de vorto en proprajn tokenojn.

    Liveras liston de tokenoj: {'tipo': 'vorto', 'segmentoj': [...]} aŭ
    {'tipo': 'interpunkcio', 'teksto': ...}.
    """
    segmentoj = [dict(s) for s in segmentoj]
    komencaj = []
    while segmentoj and segmentoj[0]['tipo'] == 'fiksa':
        teksto = segmentoj[0]['teksto']
        n = 0
        while n < len(teksto) and teksto[n] in INTERPUNKCIO:
            n += 1
        if n == 0:
            break
        komencaj.extend({'tipo': 'interpunkcio', 'teksto': c} for c in teksto[:n])
        resto = teksto[n:]
        if resto:
            segmentoj[0]['teksto'] = resto
            break
        segmentoj.pop(0)

    finaj = []
    while segmentoj and segmentoj[-1]['tipo'] == 'fiksa':
        teksto = segmentoj[-1]['teksto']
        n = len(teksto)
        while n > 0 and teksto[n - 1] in INTERPUNKCIO:
            n -= 1
        if n == len(teksto):
            break
        finaj = [{'tipo': 'interpunkcio', 'teksto': c} for c in teksto[n:]] + finaj
        resto = teksto[:n]
        if resto:
            segmentoj[-1]['teksto'] = resto
            break
        segmentoj.pop()

    tokenoj = list(komencaj)
    if segmentoj:
        tokenoj.append({'tipo': 'vorto', 'segmentoj': segmentoj})
    tokenoj.extend(finaj)
    return tokenoj


def grupigu_kompletigon(vicoj):
    """Transformu la ekzercon «Kompletigu la frazojn» en tokenojn.

    Ĉiu frazo (vico) iĝas listo de tokenoj. Vorto-tokeno havas
    «segmentoj» {'tipo': 'fiksa'|'solvo', 'teksto': ...}; interpunkcio
    estas aparta tokeno. Spacoj en la «videbla»-teksto (kaj malplenaj
    «videbla»-eroj) apartigas vortojn; «solvo»-eroj neniam apartigas,
    do ili kunfandiĝas kun najbaraj fiksaj partoj (prefikso, sufikso
    aŭ infikso de unu vorto).
    """
    frazoj = []
    for vico in vicoj:
        vortoj = []
        nuna = []

        def fini():
            if nuna:
                vortoj.append(nuna[:])
                nuna.clear()

        for parto in vico:
            if 'videbla' in parto:
                teksto = parto['videbla']
                if not teksto:
                    fini()
                    continue
                pecoj = teksto.split(' ')
                for indekso, peco in enumerate(pecoj):
                    if indekso > 0:
                        fini()
                    if peco != '':
                        nuna.append({'tipo': 'fiksa', 'teksto': peco})
            elif 'solvo' in parto:
                solvo = (parto['solvo'] or '').strip()
                if solvo != '':
                    nuna.append({'tipo': 'solvo', 'teksto': solvo})
        fini()

        tokenoj = []
        for vorto in vortoj:
            tokenoj.extend(disigi_interpunkcion(vorto))
        frazoj.append(tokenoj)
    return frazoj


def get_markdown_headlines(s):
    def purigu_titolon(markdown_titolo):
        return re.sub(r'[`*_]+', '', markdown_titolo).strip()

    uzitaj = {}
    titoloj = []
    for match in re.finditer(r'(^|\n)# (.+)\n', s):
        titolo = purigu_titolon(match.group(2))
        titolo_por_ankro = forigu_html(titolo).strip()
        titoloj.append({
            'titolo': titolo,
            'ankro': unika_ankro(titolo_por_ankro, uzitaj),
        })
    return titoloj


def load(language, gramatiko_transpose_headlines=2):
    enhavo = {'lingvo': language, 'vortaro': {}, 'tutvorta_vortaro': {}}

    tradukenda_dir = ENHAVO_DIR / 'tradukenda' / language
    netradukenda_dir = ENHAVO_DIR / 'netradukenda'
    paths = sorted((tradukenda_dir / 'vortaro').glob('*.yml'))
    # Provo solvi
    # https://github.com/Esperanto/kurso-zagreba-metodo/issues/36
    # sed kauzas aliajn problemojn.
    # paths.append('enhavo/tradukenda/en/vortaro/vorto.yml')
    # print(paths)
    for path in paths:
        vortspeco = path.stem.replace('_', ' ')
        vortlisto = legi_yaml(path)
        for esperante in vortlisto:
            fontlingve = vortlisto[esperante]
            vortlisto[esperante] = {
                'tradukajxo': fontlingve,
                'vortspeco': vortspeco
            }
        enhavo['vortaro'].update(vortlisto)

    for esperante, vortero in enhavo['vortaro'].items():
        if vortero['vortspeco'] == 'vorto':
            enhavo['tutvorta_vortaro'][esperante] = vortero

    for esperante, vortero in enhavo['vortaro'].items():
        if vortero['vortspeco'] != 'radiko':
            enhavo['tutvorta_vortaro'].setdefault(esperante, vortero)

    enhavo['finajxoj'] = legi_yaml(netradukenda_dir / 'radikaj_finajxoj.yml')

    enhavo['ordoj'] = {}
    ordoj_dir = netradukenda_dir / 'ordoj'
    enhavo['ordoj']['cifero'] = legi_yaml(ordoj_dir / 'cifero.yml')
    enhavo['ordoj']['monato'] = legi_yaml(ordoj_dir / 'monato.yml')
    enhavo['ordoj']['sezono'] = legi_yaml(ordoj_dir / 'sezono.yml')
    enhavo['ordoj']['tago_en_la_semajno'] = legi_yaml(ordoj_dir / 'tago_en_la_semajno.yml')

    enhavo['fasado'] = Fasado()
    for path in sorted((tradukenda_dir / 'fasado').glob('*.yml')):
        tradukajxoj = legi_yaml(path)
        enhavo['fasado'].update(tradukajxoj)

    path = tradukenda_dir / 'enkonduko.md'
    enkonduko = legi_tekston(path)
    # enkonduko = transpose_headlines(enkonduko, 1)
    enhavo['enkonduko'] = enkonduko

    path = tradukenda_dir / 'post.md'
    post = legi_tekston(path).strip()
    enhavo['post'] = transpose_headlines(post, 2) if post else ''

    lecionoj = []
    vortoj = set()
    lecionaj_bildoj = legi_yaml(netradukenda_dir / 'lecionaj_bildoj.yml')

    for i in LECION_NUMEROJ:
        leciono = {
            'bildo': None,
            'teksto': None,
            'gramatiko': None,
            'ekzercoj': None,
        }
        i_padded = str(i).zfill(2)

        leciono['bildo'] = lecionaj_bildoj[i_padded]

        leciono['indekso'] = {
            'cifre': i,
            'cxene': i_padded
        }

        path = netradukenda_dir / 'tekstoj' / (i_padded + '.yml')
        leciono['teksto'] = legi_yaml(path)

        leciono['teksto']['titolo_string'] = ''.join(
            ''.join(radikoj) if radikoj else ' '
            for radikoj in leciono['teksto']['titolo']
        )

        leciono['vortoj'] = {}
        leciono['vortoj']['teksto'] = []
        leciono['vortoj']['pliaj'] = []

        path = netradukenda_dir / 'vortoj' / (i_padded + '.yml')
        leciono['vortoj']['pliaj'] = legi_yaml(path)

        for paragrafo in leciono['teksto']['paragrafoj']:
            for vorto in paragrafo:
                if isinstance(vorto, list):
                    for radiko in vorto:
                        radiko_lower = radiko.lower()
                        if radiko_lower not in vortoj:
                            leciono['vortoj']['teksto'].append(radiko)
                            vortoj.add(radiko_lower)

        path = tradukenda_dir / 'gramatiko' / (i_padded + '.md')

        gramatiko_teksto = legi_tekston(path)
        gramatiko_titoloj = get_markdown_headlines(gramatiko_teksto)
        gramatiko_teksto = transpose_headlines(gramatiko_teksto, gramatiko_transpose_headlines)

        gramatiko = {
            'teksto': gramatiko_teksto,
            'titoloj': gramatiko_titoloj,
        }
        leciono['gramatiko'] = gramatiko

        ekzercoj = {}

        path = tradukenda_dir / 'ekzercoj' / 'traduku' / (i_padded + '.yml')
        ekzercoj['Traduku'] = legi_yaml(path)

        path = tradukenda_dir / 'ekzercoj' / 'traduku-kaj-respondu' / (i_padded + '.yml')
        ekzercoj['Traduku kaj respondu'] = legi_yaml(path)

        path = netradukenda_dir / 'ekzercoj' / 'kompletigu-la-frazojn' / (i_padded + '.yml')
        ekzercoj['Kompletigu la frazojn'] = grupigu_kompletigon(legi_yaml(path))

        leciono['ekzercoj'] = ekzercoj

        lecionoj.append(leciono)

    enhavo['lecionoj'] = lecionoj

    return enhavo


def get_cmdline_arguments():
    ap = argparse.ArgumentParser()
    lingvo_group = ap.add_mutually_exclusive_group(required=True)
    lingvo_group.add_argument(
        "-l",
        "--lingvo",
        help="Kreu eligon por tiu lingvo.",
        type=str
    )
    lingvo_group.add_argument(
        "--lingvoj",
        help="Kreu HTML-eligon por pluraj lingvoj per unu Python-procezo.",
        nargs='+'
    )
    lingvo_group.add_argument(
        "--cxiuj-lingvoj",
        action="store_true",
        help="Kreu HTML-eligon por ĉiuj pretaj kaj testaj lingvoj."
    )
    ap.add_argument(
        "-ef",
        "--eligformo",
        help="La eligoformo",
        type=str,
        choices=['html', 'md'],
        default='html'
    )
    ap.add_argument(
        "-pp",
        "--printendaj-partoj",
        help="Printendaj partoj",
        type=str,
        choices=['teksto', 'vortoj', 'gramatiko', 'ekzerco1', 'ekzerco2', 'ekzerco3', 'solvo1', 'solvo2', 'solvo3'],
        default=['teksto', 'vortoj', 'gramatiko', 'ekzerco1', 'ekzerco2', 'ekzerco3', 'solvo1', 'solvo2', 'solvo3'],
        nargs='*'
    )
    ap.add_argument(
        "-pl",
        "--printendaj-lecionoj",
        help="Printendaj lecionoj",
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        default=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        nargs='*'
    )
    ap.add_argument(
        "-vp",
        "--vojprefikso",
        help="La vojprefikso por ĉiuj ligiloj en la eligo. Norme: /[lingvokodo]/",
        type=str
    )
    args = ap.parse_args()
    if args.eligformo == 'md' and (args.lingvoj or args.cxiuj_lingvoj):
        ap.error('--lingvoj kaj --cxiuj-lingvoj estas uzeblaj nur kun --eligformo html')

    return args


def kompletigu_enhavon(lingvo, lingvoj, gramatiko_transpose_headlines=2):
    enhavo = load(lingvo, gramatiko_transpose_headlines)
    enhavo['lingvoj'] = lingvoj
    enhavo['tekstodirekto'] = lingvoj[lingvo].get('tekstodirekto', 'ltr')
    return enhavo


def legi_cxefpagxan_fasadon(lingvo, defauxlta_fasado=None):
    fasado = dict(defauxlta_fasado or {})
    path = ENHAVO_DIR / 'tradukenda' / lingvo / 'fasado' / 'cxefpagxo.yml'
    if path.is_file():
        fasado.update(legi_yaml(path) or {})
    return fasado


def hejmaj_lingvoj(lingvoj):
    defauxlta_fasado = legi_cxefpagxan_fasadon('en')
    rezulto = []
    for kodo in sorted(lingvoj):
        lingvo = lingvoj[kodo]
        if lingvo.get('stato') != 'preta':
            continue

        nomo = lingvo.get('nomo', {})
        fasado = legi_cxefpagxan_fasadon(kodo, defauxlta_fasado)
        rezulto.append({
            'kodo': kodo,
            'nomo': nomo.get('fontlingve', kodo),
            'esperanta_nomo': nomo.get('esperante', kodo),
            'tekstodirekto': lingvo.get('tekstodirekto', 'ltr'),
            'titolo': fasado.get(CXEFPAGXO_TITOLO, defauxlta_fasado[CXEFPAGXO_TITOLO]),
            'subtitolo': fasado.get(CXEFPAGXO_SUBTITOLO, defauxlta_fasado[CXEFPAGXO_SUBTITOLO]),
            'ek': fasado.get('Ek', defauxlta_fasado['Ek']),
        })
    return rezulto


def html_lingvoj(lingvoj):
    return [
        kodo
        for kodo, lingvo in sorted(lingvoj.items())
        if lingvo.get('stato') in HTML_LINGVO_STATOJ
    ]


def generu_html_por_lingvoj(args, lingvoj):
    por_generi = html_lingvoj(lingvoj) if args.cxiuj_lingvoj else (args.lingvoj or [args.lingvo])
    hejmaj_lingvoj_datenoj = hejmaj_lingvoj(lingvoj)
    for index, lingvo in enumerate(por_generi):
        if len(por_generi) > 1:
            print('Generas HTML por ' + lingvo, flush=True)
        enhavo = kompletigu_enhavon(lingvo, lingvoj)
        html_generilo.generate_html(
            lingvo,
            enhavo,
            args,
            kopiu_statikan=(index == 0),
            hejmaj_lingvoj=hejmaj_lingvoj_datenoj,
        )
    html_generilo.generate_seo_files(lingvoj, por_generi)
    html_generilo.generate_pwa(por_generi)


def main():
    args = get_cmdline_arguments()
    lingvoj = legi_yaml(AGORDOJ_DIR / 'lingvoj.yml')
    if args.eligformo == 'html':
        # if args.lingvo not in lingvoj.keys():
        #    sys.exit("'" + args.lingvo + "' ne estas havebla lingvokodo.")
        generu_html_por_lingvoj(args, lingvoj)
    if args.eligformo == 'md':
        enhavo = kompletigu_enhavon(args.lingvo, lingvoj, 3)
        md_generilo.kreu_md(enhavo, printendaj={'partoj': args.printendaj_partoj,
                                                'lecionoj': args.printendaj_lecionoj})


if __name__ == '__main__':
    main()
