#### {{ enhavo.fasado['Traduku'] }}

{% for vico in leciono.ekzercoj['Traduku'] %}
  {% for esperante, fontlingve in vico.items() %}
- {{ esperante }}: {% if llms %}____{% else %}`\hrulefill`{=latex}{% endif %}

  {% endfor %}
{% endfor %}
