### {{ enhavo.fasado['Novaj vortoj'] }}


{% if not llms %}
`\begin{multicols}{2}`{=latex}
{% endif %}


#### {{ enhavo.fasado['En la teksto'] or '' }}

{% for radiko in leciono.vortoj.teksto %} 
    {% include 'vortlistelemento.md' %}
{% endfor %}


#### {{ enhavo.fasado['Pliaj'] or '' }}

{% for radiko in leciono.vortoj.pliaj %} 
    {% include 'vortlistelemento.md' %}
{% endfor %}


{% if not llms %}
`\end{multicols}`{=latex}
{% endif %}
