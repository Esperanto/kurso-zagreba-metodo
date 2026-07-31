#### {{ enhavo.fasado['Kompletigu la frazojn'] }}

{% for vico in leciono.ekzercoj['Kompletigu la frazojn'] %}

{% if vico.traduko %}**{{ vico.traduko }}**
{% endif %}- {% for token in vico.tokenoj -%}
		{%- if token.tipo == 'interpunkcio' -%}
			{{ token.teksto }}
		{%- else -%}
			{%- if not loop.first %} {% endif -%}
			{%- for segmento in token.segmentoj -%}
			{%- if segmento.tipo == 'fiksa' -%}
				{{ segmento.teksto }}
			{%- else -%}
				**{{ segmento.teksto }}**
			{%- endif -%}
			{%- endfor -%}
		{%- endif -%}
	{%- endfor %}

{% endfor %}
