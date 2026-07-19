#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

import jinja2
import mistune
from markupsafe import Markup


FONTO_DIR = Path(__file__).resolve().parents[1]


def rendu_md(enhavo, printendaj, template='arangxo.md', **context):
    md = mistune.create_markdown()

    env = jinja2.Environment(auto_reload=False)
    env.filters['markdown'] = lambda text: Markup(md(text))
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.loader = jinja2.FileSystemLoader(str(FONTO_DIR / 'md'))

    rendered = env.get_template(template).render(
        enhavo=enhavo,
        printendaj=printendaj,
        **context,
    )
    return rendered


def kreu_md(enhavo, printendaj):
    print(rendu_md(enhavo, printendaj))
