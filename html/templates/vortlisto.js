var vortlisto = {
	'esperante': [
		{% for esperante in enhavo.vortaro|sort -%}
		'{{esperante}}'
		{%- if not loop.last -%}
			,
		{%- endif -%}
		{%- endfor -%}
	], 
	'fontlingve': [
		{%- for esperante in enhavo.vortaro|sort -%}
	  {%- set klavo = esperante -%}
	  '{%- include 'tradukajxo.html' -%}'
		{%- if not loop.last -%}
			,
		{%- endif -%}
		{%- endfor -%}
	]
};
