# -*- coding: utf-8 -*-

import os
import shutil

def generate_html(enhavo):

    env = jinja2.Environment()
    env.filters['markdown'] = lambda text: jinja2.Markup(md(text))
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.loader=jinja2.FileSystemLoader('html/templates/')

    rendered = env.get_template('index.html').render(enhavo=enhavo, root='')


    output_path = 'html/output/'


    with open(output_path + 'index.html', 'w') as f:
        f.write(rendered.encode('utf-8'))

    for i in range(1,13):
        i_padded = str(i).zfill(2)
        leciono_dir = output_path + i_padded
        shutil.rmtree(leciono_dir, ignore_errors=True)
        os.mkdir(leciono_dir)

        #teksto_dir = leciono_dir + '/teksto'
        #os.mkdir(teksto_dir)

        previous_path = None
        if i > 1:
            previous_path = '../' + str(i-1).zfill(2) + '/ekzerco3/'

        next_path = 'gramatiko/'
        teksto_rendered = env.get_template('teksto.html').render(
          enhavo=enhavo, 
          leciono=enhavo['lecionoj'][i-1], 
          leciono_index=i,
          root='../',
          previous_path=previous_path,
          next_path=next_path
        )
        with open(leciono_dir + '/index.html', 'w') as f:
            f.write(teksto_rendered.encode('utf-8'))

        tabs = [
          'gramatiko',
          'ekzerco1',
          'ekzerco2',
          'ekzerco3'
        ]
        for tab in tabs:
            tab_dir = leciono_dir + '/' + tab
            os.mkdir(tab_dir)

            previous_path = None
            next_path = None

            tab_rendered = env.get_template(tab + '.html').render(
              enhavo=enhavo, 
              leciono=enhavo['lecionoj'][i-1], 
              leciono_index=i,
              root='../../'
              previous_path=previous_path,
              next_path=next_path
            )
            with open(tab_dir + '/index.html', 'w') as f:
                f.write(tab_rendered.encode('utf-8'))

