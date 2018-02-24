# -*- coding: utf-8 -*-

import os
import shutil
import re

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
        True

def generate_html(lingvo, enhavo, args):

    eligo = {}

    env = jinja2.Environment()
    env.filters['markdown'] = lambda text: jinja2.Markup(md(text))
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.loader=jinja2.FileSystemLoader('html/templates/')

    output_path = 'html/output/' + lingvo + '/'


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

    # vortoj.[lingvo].tsv
    rendered = env.get_template('eksporto/anki.tsv').render(
      enhavo = enhavo,
      vojprefikso = vojprefikso,
    )
    eligo[output_path + 'eksporto/anki.tsv'] = rendered


    for tab_page in ['tabelvortoj', 'prepozicioj', 'konjunkcioj', 'afiksoj', 'diversajxoj', 'auxtoroj']:
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
        # Forigu nenecesan blankspacon.
        # Sed ne ĉe .tsv
        if not re.search(r'\.tsv$', vojo):
            eligo[vojo] = re.sub(r'\s+', ' ', eligo[vojo])
        write_file(vojo, eligo[vojo])
