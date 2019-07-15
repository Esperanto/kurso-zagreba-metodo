## {%- for vorto in leciono.teksto.titolo %} {% include 'vorto.md' %} {%- endfor %}

{% for paragrafo in leciono.teksto.paragrafoj %}

	{% for vorto in paragrafo -%}
    {%- include 'vorto.md' -%}
  {%- endfor %}

{% endfor %}

### {{ enhavo.fasado['Novaj vortoj'] }}

#### {{ enhavo.fasado['En la teksto'] }}

{% for radiko in leciono.vortoj.teksto %} 
    {% include 'vortlisto.md' %}
{% endfor %}


#### {{ enhavo.fasado['Pliaj'] }}

{% for radiko in leciono.vortoj.pliaj %} 
    {% include 'vortlisto.md' %}
{% endfor %}


### {{ enhavo.fasado['Gramatiko'] }}

{{ leciono.gramatiko.teksto }}


### {{ enhavo.fasado['Ekzercoj'] }}


#### {{ enhavo.fasado['Traduku'] }}

{% for vico in leciono.ekzercoj['Traduku'] %}
  {% for esperante, fontlingve in vico.items() %}
- {{ esperante }}:

  {% endfor %}
{% endfor %}

#### {{ enhavo.fasado['Kompletigu la frazojn'] }}

#### {{ enhavo.fasado['Traduku kaj respondu'] }}

{% for vico in leciono.ekzercoj['Traduku kaj respondu'] %}

##### {{ vico.demando }}

{% for paro in vico.rektatraduko  %}

  {%- if paro is mapping -%}
    {% for esperante, fontlingve in paro.items() %}
- {{ fontlingve }}:
    {% endfor %}
  {% endif %}

{% endfor %}

{% endfor %}
