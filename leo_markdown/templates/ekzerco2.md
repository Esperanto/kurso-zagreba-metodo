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
