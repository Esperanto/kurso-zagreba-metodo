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
				{%- for i in range(segmento.teksto|length*2) -%}\_{%- endfor -%}
			{%- endif -%}
			{%- endfor -%}
		{%- endif -%}
	{%- endfor %}

{% endfor %}
