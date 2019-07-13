#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import re
import yaml, jinja2, mistune
import genanki

def render_page(name, enhavo, vojprefikso, env, output_path):

    rendered = env.get_template(name + '.html').render(
      enhavo = enhavo,
      vojprefikso   = vojprefikso,
    )

    return rendered

def write_file(filename, content):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(filename, 'w') as f:
        f.write(content)

# Create an Anki file.
def create_anki(enhavo):

  model = genanki.Model(
    hash('Frases'),
    'Frases',
    fields=[
      {'name': 'eo' },
      {'name': enhavo['lingvo'] },
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
    hash('eo' + '-' + enhavo['lingvo']),
    'Learn Esperanto: ' + enhavo['lingvo']
  )

  for leciono_index_0 in range(len(enhavo['lecionoj'])):
    leciono = enhavo['lecionoj'][leciono_index_0]
    for radiko in leciono['vortoj']['teksto']:

      if radiko.lower() in enhavo['vortaro']:
          radiko = radiko.lower()

      esperanta_karto = radiko

      if enhavo['vortaro'][radiko]['vortspeco'] in ['interjekcio','nomo','vorto']:
          continue

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

      note = genanki.Note(
        model = model,
        tags = [str(leciono_index_0 + 1), enhavo['vortaro'][radiko]['vortspeco']],
        fields = [
            esperanta_karto,
            fontlingva_karto
        ]
      )
      deck.add_note(note)
        
  return deck


def generate_html(lingvo, enhavo, args):
    eligo = {}
    md = mistune.Markdown()

    env = jinja2.Environment()
    env.filters['markdown'] = lambda text: jinja2.Markup(md(text))
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.loader=jinja2.FileSystemLoader('html_generiloj/templates/')

    output_path = 'html_generiloj/output/' + lingvo + '/'


    tabs = [
        ('teksto'    , ''           , enhavo['fasado']['Teksto']   ) ,
        ('vortoj'    , 'vortoj/'    , enhavo['fasado']['Novaj vortoj']) ,
        ('gramatiko' , 'gramatiko/' , enhavo['fasado']['Gramatiko']) ,
        ('ekzerco1'  , 'ekzerco1/'  , enhavo['fasado']['Ekzerco 1']) ,
        ('ekzerco2'  , 'ekzerco2/'  , enhavo['fasado']['Ekzerco 2']) ,
        ('ekzerco3'  , 'ekzerco3/'  , enhavo['fasado']['Ekzerco 3'])
    ]

    if args.vojprefikso:
        vojprefikso = args.vojprefikso + lingvo + '/'
    else:
        vojprefikso = '/' + lingvo + '/'

    rendered = env.get_template('index.html').render(
      enhavo = enhavo,
      vojprefikso   = vojprefikso,
      tabs   = tabs,
    )

    eligo[output_path + 'index.html'] = rendered

    # vortaro.js
    rendered = env.get_template('vortlisto.js').render(
      enhavo = enhavo,
    )
    eligo[output_path + 'js/vortlisto.js'] = rendered

    eligo[output_path + 'eksporto/anki.apkg'] = create_anki(enhavo)

    for tab_page in ['tabelvortoj', 'prepozicioj', 'konjunkcioj', 'afiksoj', 'diversajxoj', 'auxtoroj', 'post']:
        eligo[output_path + tab_page + '/index.html'] = render_page(tab_page, enhavo, vojprefikso, env, output_path)

    paths = []
    for i in range(1, 13):
        for  id, href,caption in tabs:
            paths.append(vojprefikso + str(i).zfill(2) + '/' + href)

    paths_index = 0

    for i in range(1, 13):
        i_padded = str(i).zfill(2)
        leciono_dir = output_path + i_padded

        for tab, href, caption in tabs:

            previous_path = None
            next_path = None

            tab_vojprefikso = vojprefikso + i_padded + '/'

            if paths_index > 0:
                previous_path = paths[paths_index-1]
            if paths_index < len(paths)-1:
                next_path = paths[paths_index+1]
            paths_index += 1

            tab_rendered = env.get_template(tab + '.html').render(
              enhavo=enhavo,
              leciono=enhavo['lecionoj'][i-1],
              leciono_index=i,
              vojprefikso=vojprefikso,
              tab_vojprefikso = tab_vojprefikso,
              previous_path=previous_path,
              next_path=next_path,
              tabs=tabs,
              active_tab=tab,
              identigilo=i_padded+'/'+href
            )

            eligo[leciono_dir + '/' + href + '/' + '/index.html'] = tab_rendered

    # Forigu nunan dosierujon.
    shutil.rmtree(output_path, ignore_errors=True)

    # Kreu novajn dosierojn
    for vojo in eligo.keys():
        if re.search(r'\.apkg$', vojo):
            write_file(vojo, '')
            genanki.Package(eligo[vojo]).write_to_file(vojo)
            continue
        write_file(vojo, eligo[vojo])
