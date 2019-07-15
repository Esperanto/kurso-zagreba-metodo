## {%- for vorto in leciono.teksto.titolo %} {% include 'vorto.md' %} {%- endfor %}

{% for paragrafo in leciono.teksto.paragrafoj %}

	{% for vorto in paragrafo -%}
    {%- include 'vorto.md' -%}
  {%- endfor %}

{% endfor %}

### {{ enhavo.fasado['Gramatiko'] }}

{{ leciono.gramatiko.teksto }}
