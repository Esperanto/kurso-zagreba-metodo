## {%- for vorto in leciono.teksto.titolo %} {% include 'vorto.md' %} {%- endfor %}

{% for paragrafo in leciono.teksto.paragrafoj %}

	{% for vorto in paragrafo -%}
    {%- include 'vorto.md' -%}
  {%- endfor %}

{% endfor %}

### {{ enhavo.fasado['Novaj vortoj'] }}

#### {{ enhavo.fasado['En la teksto'] or '' }}

{% for radiko in leciono.vortoj.teksto %} 
    {% include 'vortlistelemento.md' %}
{% endfor %}


#### {{ enhavo.fasado['Pliaj'] or '' }}

{% for radiko in leciono.vortoj.pliaj %} 
    {% include 'vortlistelemento.md' %}
{% endfor %}


### {{ enhavo.fasado['Gramatiko'] }}

{{ leciono.gramatiko.teksto }}


### {{ enhavo.fasado['Ekzercoj'] }}



{% include 'ekzerco1.md' %}

{% include 'ekzerco2.md' %}

{% include 'ekzerco3.md' %}
