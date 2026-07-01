{% if 'teksto' in printendaj.partoj -%}
  {% include 'teksto.md' %}
{%- endif %}


{% if 'vortoj' in printendaj.partoj -%}
  {% include 'vortoj.md' %}
{%- endif %}


{% if 'gramatiko' in printendaj.partoj -%}
  {% include 'gramatiko.md' %}
{%- endif %}


{% if 'ekzerco1' in printendaj.partoj or 'ekzerco2' in printendaj.partoj or 'ekzerco3' in printendaj.partoj -%}

### {{ enhavo.fasado['Ekzercoj'] }}


{% if 'ekzerco1' in printendaj.partoj  -%}
{% include 'ekzerco1.md' %}
{%- endif %}

{% if 'ekzerco2' in printendaj.partoj  -%}
{% include 'ekzerco2.md' %}
{%- endif %}

{% if 'ekzerco3' in printendaj.partoj  -%}
{% include 'ekzerco3.md' %}
{%- endif %}

{%- endif %}


{% if 'solvo1' in printendaj.partoj or 'solvo2' in printendaj.partoj or 'solvo3' in printendaj.partoj -%}

### {{ enhavo.fasado['Solvoj'] or 'Solvoj' }}

{% if not llms %}
`\begin{multicols}{2}`{=latex}
{% endif %}



{% if 'solvo1' in printendaj.partoj -%}
  {% include 'solvo1.md' %}
{%- endif %}


{% if 'solvo2' in printendaj.partoj -%}
  {% include 'solvo2.md' %}
{%- endif %}


{% if 'solvo3' in printendaj.partoj -%}
  {% include 'solvo3.md' %}
{%- endif %}


{% if not llms %}
`\end{multicols}`{=latex}
{% endif %}


{% endif %}
