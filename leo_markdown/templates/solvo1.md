#### {{ enhavo.fasado['Traduku'] }}

{% for vico in leciono.ekzercoj['Traduku'] %}
  {% for esperante, fontlingve in vico.items() %}
- {{ esperante }}: {{fontlingve if fontlingve is string else fontlingve|join(', ')}}
  {% endfor %}
{% endfor %}
