# -*- coding: utf-8 -*-

import os
import shutil

def generate_html(enhavo):

    env = jinja2.Environment()
    env.filters['markdown'] = lambda text: jinja2.Markup(md(text))
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.loader=jinja2.FileSystemLoader('html/templates/')


    tabs = [
        ('teksto'    , ''           , enhavo['vortaro']['Teksto']   ) , 
        ('gramatiko' , 'gramatiko/' , enhavo['vortaro']['Gramatiko']) , 
        ('ekzerco1'  , 'ekzerco1/'  , enhavo['vortaro']['Ekzerco 1']) , 
        ('ekzerco2'  , 'ekzerco2/'  , enhavo['vortaro']['Ekzerco 2']) , 
        ('ekzerco3'  , 'ekzerco3/'  , enhavo['vortaro']['Ekzerco 3'])
    ]
    root='/esperanto-kurso-zagreba-metodo/html/output/'

    rendered = env.get_template('index.html').render(
      enhavo = enhavo,
      root   = root,
      tabs   = tabs,
    )


    output_path = 'html/output/'


    with open(output_path + 'index.html', 'w') as f:
        f.write(rendered.encode('utf-8'))

    paths = []
    for i in range(1, 13):
        for  id, href,caption in tabs:
            paths.append(root + str(i).zfill(2) + '/' + href)

    paths_index = 0

    for i in range(1,13):
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

            tab_root = root + i_padded + '/'

            if paths_index > 0:
                previous_path = paths[paths_index-1]
            if paths_index < len(paths)-1:
                next_path = paths[paths_index+1]
            paths_index += 1

            tab_rendered = env.get_template(tab + '.html').render(
              enhavo=enhavo, 
              leciono=enhavo['lecionoj'][i-1], 
              leciono_index=i,
              root=root,
              tab_root = tab_root,
              previous_path=previous_path,
              next_path=next_path,
              tabs=tabs,
              active_tab=tab
            )
            with open(tab_dir + '/index.html', 'w') as f:
                f.write(tab_rendered.encode('utf-8'))

