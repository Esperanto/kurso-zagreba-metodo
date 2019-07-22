### {{ enhavo.fasado['Novaj vortoj'] }}


`\begin{multicols}{2}`{=latex}


#### {{ enhavo.fasado['En la teksto'] or '' }}

{% for radiko in leciono.vortoj.teksto %} 
    {% include 'vortlistelemento.md' %}
{% endfor %}


#### {{ enhavo.fasado['Pliaj'] or '' }}

{% for radiko in leciono.vortoj.pliaj %} 
    {% include 'vortlistelemento.md' %}
{% endfor %}


`\end{multicols}`{=latex}

