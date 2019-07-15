---
title: {{ enhavo.fasado['Lerni Esperanton'] or enhavo.fasado['Esperanto en 12 tagoj'] }}
subtitle: {{enhavo.fasado['La plej rapida kurso por la bazoj']}}
documentclass: scrartcl
toc: True
fontsize: 12pt
'toc-depth': 2
---

# Enkonduko

{{enhavo.enkonduko}}

# Lecionoj

{% for leciono in enhavo.lecionoj %}
  {% include 'leciono.md' %}
{% endfor %}
