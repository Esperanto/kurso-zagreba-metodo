{% if 'teksto' in partoj -%}
  {% include 'teksto.md' %}
{%- endif %}


{% if 'vortoj' in partoj -%}
  {% include 'vortoj.md' %}
{%- endif %}


{% if 'vortoj' in partoj -%}
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
