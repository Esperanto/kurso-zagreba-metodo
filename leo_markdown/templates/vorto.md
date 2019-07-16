{%- if vorto is string -%}
  {%- if vorto in [',','.'] -%}
    {{vorto}}
  {%- else -%} 
    {{vorto}}
{%- endif -%} 
{%- elif vorto is iterable -%}
  {{vorto|join}}
{%- else %} {% endif -%} 
