#### {{ enhavo.fasado['Kompletigu la frazojn'] }}

{% for vico in leciono.ekzercoj['Kompletigu la frazojn'] %}

- {% for vorto in vico -%}
		{%- for segmento in vorto -%}
			{%- if segmento.tipo == 'fiksa' -%}
				{{ segmento.teksto }}
			{%- else -%}
				{%- for i in range(segmento.teksto|length*2) -%}\_{%- endfor -%}
			{%- endif -%}
		{%- endfor %} {% endfor %}

{% endfor %}
