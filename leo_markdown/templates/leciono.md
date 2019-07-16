{% if 'teksto' in partoj -%}
  {% include 'teksto.md' %}
{%- endif %}


{% if 'vortoj' in partoj -%}
  {% include 'vortoj.md' %}
{%- endif %}


{% if 'gramatiko' in partoj -%}
  {% include 'gramatiko.md' %}
{%- endif %}


{% if 'ekzerco1' in partoj or 'ekzerco2' in partoj or 'ekzerco3' in partoj -%}

### {{ enhavo.fasado['Ekzercoj'] }}


{% if 'ekzerco1' in partoj  -%}
{% include 'ekzerco1.md' %}
{%- endif %}

{% if 'ekzerco2' in partoj  -%}
{% include 'ekzerco2.md' %}
{%- endif %}

{% if 'ekzerco3' in partoj  -%}
{% include 'ekzerco3.md' %}
{%- endif %}

{%- endif %}


{% if 'solvo1' in partoj or 'solvo2' in partoj or 'solvo3' in partoj -%}

### {{ enhavo.fasado['Solvoj'] or 'Solvoj' }}


{% if 'solvo1' in partoj -%}
  {% include 'solvo1.md' %}
{%- endif %}


{% if 'solvo2' in partoj -%}
  {% include 'solvo2.md' %}
{%- endif %}


{% if 'solvo3' in partoj -%}
  {% include 'solvo3.md' %}
{%- endif %}


{%- endif %}
