# -*- coding: utf-8 -*-

import yaml
import jinja2
import glob
import re
import mistune
import os
import sys
import argparse


def transpose_headlines(markdown, level):
    prefix = ''
    for i in range(level):
        prefix += '#'
    markdown = re.sub(r'^#', '#' + prefix, markdown)
    markdown = re.sub(r'\n#', '\n#' + prefix, markdown)
    return markdown 


def get_markdown_headlines(s):

    headlines = []
    for match in  re.finditer(r'(^|\n)# (.+)\n', s):
        headlines.append(match.group(2).strip())

    return headlines


def load(language):

    enhavo = {}
    enhavo['lingvo'] = language
    enhavo['vortaro'] = {}

    paths = glob.glob('enhavo/tradukenda/' + language + '/vortaro/*.yml')
    for path in paths:
        dirs, filename = os.path.split(path)
        root, extension = os.path.splitext(filename)
        vortspeco = root.replace('_', ' ')
        vortlisto = yaml.load(open(path).read())
        for esperante in vortlisto:
            fontlingve = vortlisto[esperante]
            vortlisto[esperante] = {
                'tradukajxo': fontlingve,
                'vortspeco': vortspeco
            }
        enhavo['vortaro'].update(vortlisto)

    enhavo['finajxoj'] = yaml.load(open('enhavo/netradukenda/radikaj_finajxoj.yml').read())

    enhavo['ordoj'] = {}
    enhavo['ordoj']['cifero'] = yaml.load(open('enhavo/netradukenda/ordoj/cifero.yml'))
    enhavo['ordoj']['monato'] = yaml.load(open('enhavo/netradukenda/ordoj/monato.yml'))
    enhavo['ordoj']['sezono'] = yaml.load(open('enhavo/netradukenda/ordoj/sezono.yml'))
    enhavo['ordoj']['tago_en_la_semajno'] = yaml.load(open('enhavo/netradukenda/ordoj/tago_en_la_semajno.yml'))

    enhavo['fasado'] = {}
    paths = glob.glob('enhavo/tradukenda/' + language + '/fasado/*.yml')
    for path in paths:
        tradukajxoj = yaml.load(open(path).read())
        enhavo['fasado'].update(tradukajxoj)

    path = 'enhavo/tradukenda/' + language + '/enkonduko.md'

    enkonduko = open(path).read()
    #enkonduko = transpose_headlines(enkonduko, 1)

    enhavo['enkonduko'] = enkonduko

    lecionoj = []
    vortoj = {}

    for i in range(1,13):
        leciono = {
            'teksto': None,
            'gramatiko': None,
            'ekzercoj': None,
        }
        i_padded = str(i).zfill(2)
        
        leciono['indekso'] = {
            'cifre': i,
            'cxene': i_padded
        }

        path = 'enhavo/netradukenda/tekstoj/' + i_padded + '.yml'
        leciono['teksto'] = yaml.load(open(path).read())

        # Create a string of the lesson titles.
        titolo_string = ''
        for radikoj in leciono['teksto']['titolo']:
            if radikoj:
                titolo_string += ''.join(radikoj)
            else:
                titolo_string += ' '
        
        leciono['teksto']['titolo_string'] = titolo_string

        leciono['vortoj'] = {}
        leciono['vortoj']['teksto'] = []
        leciono['vortoj']['pliaj'] = []

        path = 'enhavo/netradukenda/vortoj/' + i_padded + '.yml'
        leciono['vortoj']['pliaj'] = yaml.load(open(path).read())

        for paragrafo in leciono['teksto']['paragrafoj']:
            for vorto in paragrafo:
                if type(vorto) is list:
                    for radiko in vorto:
                        if not radiko.lower() in vortoj:
                            leciono['vortoj']['teksto'].append(radiko)
                            vortoj[radiko.lower()] = True

        path = 'enhavo/tradukenda/' + language + '/gramatiko/' + i_padded + '.md'

        gramatiko_teksto = open(path).read()
        gramatiko_titoloj = get_markdown_headlines(gramatiko_teksto)
        gramatiko_teksto = transpose_headlines(gramatiko_teksto, 2)

        gramatiko = {
            'teksto': gramatiko_teksto,
            'titoloj': gramatiko_titoloj,
        }
        leciono['gramatiko'] = gramatiko

        ekzercoj = {}

        path = 'enhavo/tradukenda/' + language + '/ekzercoj/traduku/' + i_padded + '.yml'
        ekzercoj['Traduku'] = yaml.load(open(path))

        path = 'enhavo/tradukenda/' + language + '/ekzercoj/traduku-kaj-respondu/' + i_padded + '.yml'
        ekzercoj['Traduku kaj respondu'] = yaml.load(open(path))

        path = 'enhavo/netradukenda/ekzercoj/kompletigu-la-frazojn/' + i_padded + '.yml'
        ekzercoj['Kompletigu la frazojn'] = yaml.load(open(path))


        # Covert from dict to list.
        leciono['ekzercoj'] = ekzercoj

        lecionoj.append(leciono)

    enhavo['lecionoj'] = lecionoj

    return enhavo

md = mistune.Markdown()
exec(open("./html/main.py").read())

ap = argparse.ArgumentParser()

ap.add_argument(
    "-vp", 
    "--vojprefikso", 
    help="La vojprefikso por ĉiuj ligiloj en la eligo. Norme: /[lingvokodo]/",
    type=str
)

ap.add_argument(
    "-l", 
    "--lingvo", 
    help="Kreu eligon nur por tiu lingvo. Norme: Kreu por ĉiujn.",
    type=str
)

args = ap.parse_args()

lingvoj = yaml.load(open('agordoj/lingvoj.yml').read())

if args.lingvo:
    #if args.lingvo not in lingvoj.keys():
    #    sys.exit("'" + args.lingvo + "' ne estas havebla lingvokodo.")
    enhavo = load(args.lingvo)
    enhavo['lingvoj'] = lingvoj
    generate_html(args.lingvo, enhavo, args)
else:
    for lingvo in lingvoj:
        enhavo = load(lingvo)
        enhavo['lingvoj'] = lingvoj
        generate_html(lingvo, enhavo, args)

