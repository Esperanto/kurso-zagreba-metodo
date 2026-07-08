#### {{ enhavo.fasado['Traduku kaj respondu'] }}

{% for vico in leciono.ekzercoj['Traduku kaj respondu'] %}

##### {{ vico.demando }}

{% for paro in vico.rektatraduko  %}

  {%- if paro is mapping -%}
    {% for esperante, fontlingve in paro.items() %}
- {{ fontlingve }}: {% if llms %}____{% else %}`\hrulefill`{=latex}{% endif %}
    {% endfor %}
  {% endif %}

{% endfor %}

{% endfor %}
