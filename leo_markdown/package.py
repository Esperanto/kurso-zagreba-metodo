#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import jinja2
import mistune


def kreu_md(enhavo, printendaj):
    md = mistune.Markdown()

    env = jinja2.Environment()
    env.filters['markdown'] = lambda text: jinja2.Markup(md(text))
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.loader=jinja2.FileSystemLoader('leo_markdown/templates/')

    # Ŝanĝu __ al **, ĉar nur tio Pandoc ŝajne komprenas.
    for i in range(len(enhavo['lecionoj'])):
        enhavo['lecionoj'][i]['gramatiko']['teksto'] = re.sub('__', '**', enhavo['lecionoj'][i]['gramatiko']['teksto'] )

    rendered = env.get_template('arangxo.md').render(enhavo=enhavo, printendaj=printendaj)
    print(rendered)
