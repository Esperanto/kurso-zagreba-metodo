# -*- coding: utf-8 -*-

import yaml
import jinja2
import markdown
import glob

def load(language):

    enhavo = {}
    enhavo['vortaro'] = {}

    filenames = glob.glob('enhavo/tradukenda/' + language + '/vortaro/*.yml')
    for filename in filenames:
        vortlisto = yaml.load(file(filename, 'r'))
        enhavo['vortaro'].update(vortlisto)

    lecionoj = []

    for i in range(1,13):
        leciono = {
          'teksto': None,
          'gramatiko': None,
          'ekzercoj': None,
        }
        i_padded = str(i).zfill(2)

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

        filename = 'enhavo/tradukenda/' + language + '/gramatiko/' + i_padded + '.yml'
        leciono['gramatiko'] = yaml.load(file(filename, 'r'))

        filename = 'enhavo/tradukenda/' + language + '/ekzercoj/' + i_padded + '.yml'
        ekzercoj1 = yaml.load(file(filename, 'r'))

        filename = 'enhavo/netradukenda/ekzercoj/' + i_padded + '.yml'
        ekzercoj2 = yaml.load(file(filename, 'r'))

        # Merge ekzercoj.
        ekzercoj = ekzercoj1.copy()
        ekzercoj.update(ekzercoj2)

        # Covert from dict to list.
        leciono['ekzercoj'] = []
        for key in sorted(ekzercoj.keys()):
            leciono['ekzercoj'].append(ekzercoj[key])

        lecionoj.append(leciono)

    enhavo['lecionoj'] = lecionoj

    return enhavo

enhavo = load('de')

md = markdown.Markdown(extensions=['meta'])

execfile('html/main.py')
generate_html(enhavo)
