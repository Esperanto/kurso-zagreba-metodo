# {{ enhavo.fasado.get('Lerni Esperanton') or enhavo.fasado.get('Lerni Esperanton en 12 lecionoj') or 'Lerni Esperanton' }}

{{enhavo.enkonduko}}

# {{ enhavo.fasado.get('Lecionoj') or 'Lecionoj' }}

{% for leciono in enhavo.lecionoj %}
  {% if loop.index in printendaj.lecionoj %}
    {% include 'leciono.md' %}
  {% endif %}
{% endfor %}
