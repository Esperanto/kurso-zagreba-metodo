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
        vortlisto = yaml.load(file(path, 'r'))
        for esperante in vortlisto:
            fontlingve = vortlisto[esperante]
            vortlisto[esperante] = {
                'tradukajxo': fontlingve,
                'vortspeco': vortspeco
            }
        enhavo['vortaro'].update(vortlisto)

    enhavo['fasado'] = {}
    paths = glob.glob('enhavo/tradukenda/' + language + '/fasado/*.yml')
    for path in paths:
        tradukajxoj = yaml.load(file(path, 'r'))
        enhavo['fasado'].update(tradukajxoj)

    path = 'enhavo/tradukenda/' + language + '/enkonduko.md'

    enkonduko = file(path, 'r').read()
    enkonduko = unicode(enkonduko, 'utf-8')
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
        leciono['teksto'] = yaml.load(file(path, 'r'))

        # Create a string of the lesson titles.
        titolo_string = ''
        for radikoj in leciono['teksto']['titolo']:
            if radikoj:
                titolo_string += ''.join(radikoj)
            else:
                titolo_string += ' '
        
        leciono['teksto']['titolo_string'] = titolo_string



        leciono['vortoj'] = []

        for paragrafo in leciono['teksto']['paragrafoj']:
            for vorto in paragrafo:
                if type(vorto) is list:
                    for radiko in vorto:
                        if not radiko.lower() in vortoj:
                            leciono['vortoj'].append(radiko)
                            vortoj[radiko.lower()] = True

        path = 'enhavo/tradukenda/' + language + '/gramatiko/' + i_padded + '.md'

        gramatiko_teksto = file(path, 'r').read()
        gramatiko_teksto = unicode(gramatiko_teksto, 'utf-8')
        gramatiko_titoloj = get_markdown_headlines(gramatiko_teksto)
        gramatiko_teksto = transpose_headlines(gramatiko_teksto, 2)

        gramatiko = {
            'teksto': gramatiko_teksto,
            'titoloj': gramatiko_titoloj,
        }
        leciono['gramatiko'] = gramatiko

        ekzercoj = {}

        path = 'enhavo/tradukenda/' + language + '/ekzercoj/traduku/' + i_padded + '.yml'
        ekzercoj['Traduku'] = yaml.load(file(path, 'r'))

        path = 'enhavo/tradukenda/' + language + '/ekzercoj/traduku-kaj-respondu/' + i_padded + '.yml'
        ekzercoj['Traduku kaj respondu'] = yaml.load(file(path, 'r'))

        path = 'enhavo/netradukenda/ekzercoj/kompletigu-la-frazojn/' + i_padded + '.yml'
        ekzercoj['Kompletigu la frazojn'] = yaml.load(file(path, 'r'))


        # Covert from dict to list.
        leciono['ekzercoj'] = ekzercoj

        lecionoj.append(leciono)

    enhavo['lecionoj'] = lecionoj

    return enhavo

md = mistune.Markdown()
execfile('html/main.py')

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

lingvoj = [
  ('ca', u'Català'),
  ('de', u'Deutsch'),
  ('en', u'English'),
  ('fr', u'Français'),
  ('es', u'Español'),
  ('ms', u'Bahasa Melayu'),
  ('pt', u'Português'),
  ('th', u'ภาษาไทย'),
  ('tr', u'Türkçe (beta)'),
  ('uk', u'Українська'),
  ('zh', u'中文'),
  ('ar', u'(test: araba)'),
  ('cs', u'(test: ĉeĥa)'),
  ('fa', u'(test: persa)'),
  ('frp', u'(test: arpitana)'),
  ('hr', u'(test: kroata)'),
  ('hu', u'(test: hungara)'),
  ('id', u'(test: indonezia)'),
  ('km', u'(test: kmera)'),
  ('ko', u'(test: korea)'),
  ('lo', u'(test: laosa)'),
  ('my', u'(test: birma)'),
  ('nl', u'(test: nederlanda)'), # Nederlands  
  ('pl', u'(test: pola)'),
  ('ru', u'(test: rusa)'),
  ('sv', u'(test: sveda)'),
  ('ur', u'(test: urdua)'),
  ('zh-tw', u'(test: tradicia ĉina)')
]

if args.lingvo:
    #if args.lingvo not in lingvoj.keys():
    #    sys.exit("'" + args.lingvo + "' ne estas havebla lingvokodo.")
    enhavo = load(args.lingvo)
    enhavo['lingvoj'] = lingvoj
    generate_html(args.lingvo, enhavo, args)
else:
    for lingvo_tuple in lingvoj:
        lingvo = lingvo_tuple[0]
        enhavo = load(lingvo)
        enhavo['lingvoj'] = lingvoj
        generate_html(lingvo, enhavo, args)

