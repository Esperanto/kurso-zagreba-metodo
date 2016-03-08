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
		{% for esperante in enhavo.vortaro|sort -%}
		'{{enhavo.vortaro[esperante].tradukajxo}}'
		{%- if not loop.last -%}
			,
		{%- endif -%}
		{%- endfor -%}
	]
};
