# -*- coding: utf-8 -*-

import yaml
import jinja2
import pprint
import markdown


def pp(data):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)


enhavo = {}
filename = 'enhavo/tradukenda/de/vortaro.yml'
enhavo['vortaro'] = yaml.load(file(filename, 'r'))

lecionoj = []

for i in range(1,2):
    leciono = {
      'teksto': None,
      'gramatiko': None,
      'ekzercoj': None,
    }
    i_padded = str(i).zfill(2)

    filename = 'enhavo/netradukenda/tekstoj/' + i_padded + '.yml'
    leciono['teksto'] = yaml.load(file(filename, 'r'))

    filename = 'enhavo/tradukenda/de/gramatiko/' + i_padded + '.yml'
    leciono['gramatiko'] = yaml.load(file(filename, 'r'))

    filename = 'enhavo/tradukenda/de/ekzercoj/' + i_padded + '.yml'
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


#pp(lecionoj)

md = markdown.Markdown(extensions=['meta'])

env = jinja2.Environment()
env.filters['markdown'] = lambda text: jinja2.Markup(md.convert(text))
env.trim_blocks = True
env.lstrip_blocks = True
env.loader=jinja2.FileSystemLoader('html/templates/')

rendered = env.get_template('index.html').render(lecionoj=lecionoj, enhavo=enhavo)
print rendered.encode('utf-8')
