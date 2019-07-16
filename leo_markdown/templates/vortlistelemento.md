-
  {%- if radiko|lower in enhavo.vortaro -%}
    {% set klavo = radiko|lower %}
    *{{radiko|lower}}
    {%- elif radiko in enhavo.vortaro -%}
    {% set klavo = radiko %}
    *{{radiko}}
    {%- else -%}
    *{% set klavo = '' %}
  {%- endif -%} 
  {%- if radiko|lower in enhavo.finajxoj -%}
    {{enhavo.finajxoj[radiko|lower]}}
  {%- endif %}* – {% include 'tradukajxo.md' %}
