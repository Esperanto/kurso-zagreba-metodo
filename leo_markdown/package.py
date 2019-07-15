#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import re
import yaml, jinja2, mistune

def kreu_md(enhavo):
  md = mistune.Markdown()

  env = jinja2.Environment()
  env.filters['markdown'] = lambda text: jinja2.Markup(md(text))
  env.trim_blocks = True
  env.lstrip_blocks = True
  env.loader=jinja2.FileSystemLoader('leo_markdown/templates/')

  rendered = env.get_template('arangxo.md').render(enhavo = enhavo)
  print(rendered)
