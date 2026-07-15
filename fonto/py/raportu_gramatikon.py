#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import re
import sys

from .generu import ROOT_DIR
from .generu import legi_yaml


LECIONOJ = tuple(f'{numero:02}' for numero in range(1, 13))
TEMOJ_DIR = ROOT_DIR / 'specifoj' / 'tradukenda' / 'gramatiko'
TRADUKENDA_DIR = ROOT_DIR / 'enhavo' / 'tradukenda'


class AgordaEraro(Exception):
    pass


def normaligu_tekston(teksto):
    teksto = teksto.lower()
    teksto = re.sub(r'[`*_]+', '', teksto)
    teksto = teksto.replace('\u00a0', ' ')
    teksto = re.sub(r'\s+', ' ', teksto)
    return teksto.strip()


def legu_temon_matricon(path=TEMOJ_DIR):
    if not path.is_dir():
        raise AgordaEraro(f'mankas gramatika tem-dosierujo: {path}')

    matrico = {}
    for leciono in LECIONOJ:
        leciona_path = path / f'{leciono}.yml'
        try:
            matrico[leciono] = legi_yaml(leciona_path)
        except Exception as error:
            raise AgordaEraro(f'ne eblas legi {leciona_path}: {error}') from error

    kontrolu_matricon(matrico, path)
    return matrico


def kontrolu_matricon(matrico, path):
    if not isinstance(matrico, dict):
        raise AgordaEraro(f'{path} devas enhavi mapon de lecionoj')

    for leciono in LECIONOJ:
        temoj = matrico[leciono]
        if not isinstance(temoj, list) or not temoj:
            raise AgordaEraro(f'{path}: leciono {leciono} devas enhavi liston de temoj')

        uzitaj_id = set()
        for temo in temoj:
            if not isinstance(temo, dict):
                raise AgordaEraro(f'{path}: temo en leciono {leciono} ne estas mapo')
            temo_id = temo.get('id')
            ankroj = temo.get('ankroj')
            if not isinstance(temo_id, str) or not temo_id:
                raise AgordaEraro(f'{path}: temo en leciono {leciono} bezonas id')
            if temo_id in uzitaj_id:
                raise AgordaEraro(f'{path}: duobla temo-id {temo_id} en leciono {leciono}')
            uzitaj_id.add(temo_id)
            if not isinstance(ankroj, list) or not ankroj:
                raise AgordaEraro(f'{path}: temo {temo_id} bezonas ankro-liston')
            if not all(isinstance(ankro, str) and ankro for ankro in ankroj):
                raise AgordaEraro(f'{path}: temo {temo_id} enhavas nevalidan ankron')


def lingvoj_por_raporto(lingvo=None):
    if lingvo:
        gramatiko_dir = TRADUKENDA_DIR / lingvo / 'gramatiko'
        if not gramatiko_dir.is_dir():
            raise FileNotFoundError(f'mankas gramatika dosierujo: {gramatiko_dir}')
        return [lingvo]

    return sorted(
        path.parent.name
        for path in TRADUKENDA_DIR.glob('*/gramatiko')
        if path.is_dir()
    )


def legu_gramatikon(lingvo, leciono):
    path = TRADUKENDA_DIR / lingvo / 'gramatiko' / f'{leciono}.md'
    if not path.is_file():
        raise FileNotFoundError(f'mankas gramatika dosiero: {path}')
    teksto = path.read_text(encoding='utf-8-sig')
    return path, teksto


def mankantaj_temoj(teksto, temoj):
    normaligita = normaligu_tekston(teksto)
    mankantaj = []
    for temo in temoj:
        mankantaj_ankroj = [
            ankro
            for ankro in temo['ankroj']
            if normaligu_tekston(ankro) not in normaligita
        ]
        if mankantaj_ankroj:
            mankantaj.append(temo['id'])
    return mankantaj


def linioj(teksto):
    return len(teksto.splitlines())


def linia_komparo(linioj_lingvo, linioj_angla):
    if linioj_angla == 0:
        return f'{linioj_lingvo}/0'
    procento = round(linioj_lingvo / linioj_angla * 100)
    return f'{linioj_lingvo}/{linioj_angla} ({procento}%)'


def kolektu_raporton(lingvoj, matrico):
    anglaj_linioj = {}
    for leciono in LECIONOJ:
        _, angla_teksto = legu_gramatikon('en', leciono)
        anglaj_linioj[leciono] = linioj(angla_teksto)

    dosieroj = 0
    temoj_total = 0
    mankantaj_vicoj = []
    for lingvo in lingvoj:
        for leciono in LECIONOJ:
            _, teksto = legu_gramatikon(lingvo, leciono)
            dosieroj += 1
            temoj_total += len(matrico[leciono])
            mankantaj = mankantaj_temoj(teksto, matrico[leciono])
            if mankantaj:
                mankantaj_vicoj.append({
                    'lingvo': lingvo,
                    'leciono': leciono,
                    'linioj': linia_komparo(linioj(teksto), anglaj_linioj[leciono]),
                    'mankantaj': ', '.join(mankantaj),
                })

    return {
        'dosieroj': dosieroj,
        'lingvoj': len(lingvoj),
        'temoj': temoj_total,
        'mankantaj_vicoj': mankantaj_vicoj,
    }


def presu_raporton(raporto):
    print('# Raporto pri gramatika temkovro')
    print()
    print(f'- Lingvoj: {raporto["lingvoj"]}')
    print(f'- Dosieroj: {raporto["dosieroj"]}')
    print(f'- Kontrolitaj temoj: {raporto["temoj"]}')
    print(f'- Vicoj kun mankantaj temoj: {len(raporto["mankantaj_vicoj"])}')
    print()

    if not raporto['mankantaj_vicoj']:
        print('Neniu mankanta temo trovita.')
        return

    print('| Lingvo | Leciono | Linioj/en | Mankantaj temoj |')
    print('| --- | --- | ---: | --- |')
    for vico in raporto['mankantaj_vicoj']:
        print(
            f'| {vico["lingvo"]} | {vico["leciono"]} | '
            f'{vico["linioj"]} | {vico["mankantaj"]} |'
        )


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Raportu mankantajn temojn en gramatikaj Markdown-dosieroj.'
    )
    parser.add_argument(
        '--lingvo',
        help='limigu la raporton al unu lingvo, ekzemple lt',
    )
    args = parser.parse_args(argv)

    try:
        matrico = legu_temon_matricon()
        lingvoj = lingvoj_por_raporto(args.lingvo)
        raporto = kolektu_raporton(lingvoj, matrico)
    except (AgordaEraro, OSError, FileNotFoundError) as error:
        print(f'Gramatika raporto malsukcesis: {error}', file=sys.stderr)
        return 1

    presu_raporton(raporto)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
