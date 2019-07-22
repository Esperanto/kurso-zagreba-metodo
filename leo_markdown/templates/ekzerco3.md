#### {{ enhavo.fasado['Traduku kaj respondu'] }}

{% for vico in leciono.ekzercoj['Traduku kaj respondu'] %}

##### {{ vico.demando }}

{% for paro in vico.rektatraduko  %}

  {%- if paro is mapping -%}
    {% for esperante, fontlingve in paro.items() %}
- {{ fontlingve }}: `\hrulefill`{=latex}
    {% endfor %}
  {% endif %}

{% endfor %}

{% endfor %}
