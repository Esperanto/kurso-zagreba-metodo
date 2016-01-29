# -*- coding: utf-8 -*-

import yaml
import jinja2
import markdown
import glob
import re
import mistune

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

    filenames = glob.glob('enhavo/tradukenda/' + language + '/vortaro/*.yml')
    for filename in filenames:
        vortlisto = yaml.load(file(filename, 'r'))
        enhavo['vortaro'].update(vortlisto)


    enhavo['fasado'] = {}
    filenames = glob.glob('enhavo/tradukenda/' + language + '/fasado/*.yml')
    for filename in filenames:
        tradukajxoj = yaml.load(file(filename, 'r'))
        enhavo['fasado'].update(tradukajxoj)

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

        filename = 'enhavo/netradukenda/tekstoj/' + i_padded + '.yml'
        leciono['teksto'] = yaml.load(file(filename, 'r'))

        # Create a string of the lesson titles.
        titolo_string = ''
        for radikoj in leciono['teksto']['titolo']:
            if radikoj:
                titolo_string += ''.join(radikoj)
            else:
                titolo_string += ' '
        
        leciono['teksto']['titolo_string'] = titolo_string

        filename = 'enhavo/tradukenda/' + language + '/gramatiko/' + i_padded + '.md'

        gramatiko_teksto = file(filename, 'r').read()
        gramatiko_teksto = unicode(gramatiko_teksto, 'utf-8')
        gramatiko_titoloj = get_markdown_headlines(gramatiko_teksto)
        gramatiko_teksto = transpose_headlines(gramatiko_teksto, 2)


        gramatiko = {
            'teksto': gramatiko_teksto,
            'titoloj': gramatiko_titoloj,
        }
        leciono['gramatiko'] = gramatiko

        ekzercoj = {}

        filename = 'enhavo/tradukenda/' + language + '/ekzercoj/traduku/' + i_padded + '.yml'
        ekzercoj['Traduku'] = yaml.load(file(filename, 'r'))

        filename = 'enhavo/tradukenda/' + language + '/ekzercoj/traduku-kaj-respondu/' + i_padded + '.yml'
        ekzercoj['Traduku kaj respondu'] = yaml.load(file(filename, 'r'))

        filename = 'enhavo/netradukenda/ekzercoj/kompletigu-la-frazojn/' + i_padded + '.yml'
        ekzercoj['Kompletigu la frazojn'] = yaml.load(file(filename, 'r'))


        # Covert from dict to list.
        leciono['ekzercoj'] = ekzercoj

        lecionoj.append(leciono)

    enhavo['lecionoj'] = lecionoj

    return enhavo

paths = []


enhavo = load('de')

md = mistune.Markdown()

execfile('html/main.py')
generate_html(enhavo)
