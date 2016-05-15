# -*- coding: utf-8 -*-

import os
import shutil

def render_page(name, enhavo, vojprefikso, env, output_path):

    rendered = env.get_template(name + '.html').render(
      enhavo = enhavo,
      vojprefikso   = vojprefikso,
    )

    dir = output_path + name + '/'
    os.mkdir(dir)
    with open(dir + 'index.html', 'w') as f:
        f.write(rendered.encode('utf-8'))

def generate_html(lingvo, enhavo, args):

    env = jinja2.Environment()
    env.filters['markdown'] = lambda text: jinja2.Markup(md(text))
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.loader=jinja2.FileSystemLoader('html/templates/')

    output_path = 'html/output/' + lingvo + '/'

    shutil.rmtree(output_path, ignore_errors=True)
    os.mkdir(output_path)

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

    with open(output_path + 'index.html', 'w') as f:
        f.write(rendered.encode('utf-8'))

    # vortaro.js
    rendered = env.get_template('vortlisto.js').render(
      enhavo = enhavo,
    )

    dir = output_path + 'js/'
    os.mkdir(dir)

    with open(dir + 'vortlisto.js', 'w') as f:
        f.write(rendered.encode('utf-8'))

    render_page('tabelvortoj', enhavo, vojprefikso, env, output_path)
    render_page('prepozicioj', enhavo, vojprefikso, env, output_path)
    render_page('konjunkcioj', enhavo, vojprefikso, env, output_path)
    render_page('afiksoj', enhavo, vojprefikso, env, output_path)
    render_page('diversajxoj', enhavo, vojprefikso, env, output_path)

    paths = []
    for i in range(1, 13):
        for  id, href,caption in tabs:
            paths.append(vojprefikso + str(i).zfill(2) + '/' + href)

    paths_index = 0

    for i in range(1, 13):
        i_padded = str(i).zfill(2)
        leciono_dir = output_path + i_padded
        shutil.rmtree(leciono_dir, ignore_errors=True)
        os.mkdir(leciono_dir)

        #teksto_dir = leciono_dir + '/teksto'
        #os.mkdir(teksto_dir)


        for tab, href, caption in tabs:
            tab_dir = leciono_dir + '/' + href + '/'
            if not os.path.exists(tab_dir):
                os.mkdir(tab_dir)

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
              active_tab=tab
            )
            with open(tab_dir + '/index.html', 'w') as f:
                f.write(tab_rendered.encode('utf-8'))

