# -*- coding: utf-8 -*-

import yaml
import jinja2
import glob
import re
import mistune
import os

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

enhavo = load('de')

md = mistune.Markdown()

execfile('html/main.py')
generate_html(enhavo)
