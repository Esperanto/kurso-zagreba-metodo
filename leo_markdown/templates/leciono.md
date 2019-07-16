## {%- for vorto in leciono.teksto.titolo %} {% include 'vorto.md' %} {%- endfor %}

{% for paragrafo in leciono.teksto.paragrafoj %}

	{% for vorto in paragrafo -%}
    {%- include 'vorto.md' -%}
  {%- endfor %}

{% endfor %}

### {{ enhavo.fasado['Novaj vortoj'] }}

#### {{ enhavo.fasado['En la teksto'] }}

{% for radiko in leciono.vortoj.teksto %} 
    {% include 'vortlistelemento.md' %}
{% endfor %}


#### {{ enhavo.fasado['Pliaj'] }}

{% for radiko in leciono.vortoj.pliaj %} 
    {% include 'vortlistelemento.md' %}
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

{% for vico in leciono.ekzercoj['Kompletigu la frazojn'] %}

- {% for parto in vico -%}
		{% set parto_loop = loop %}
		{%- for klavo,valoro in parto.items() -%}
			{%- if klavo == 'videbla' -%}
				{%- if valoro -%}
					{{valoro}}
				{%- else %} {% endif -%} 
			{%- elif klavo == 'solvo' -%}
		    {%- for i in range(valoro|length*2) -%}
          \_
	      {%- endfor -%}
			{%- endif -%} 
	 {%- endfor %}
	{% endfor %}

{% endfor %}

{% include 'ekzerco3.md' %}
