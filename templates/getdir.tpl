{% if rs.dir %}

{% for r in rs.children %}
[x] - key: <a href="{{ r.key }}">{{ r.key }}</a></br>
{% endfor %}

{% else %}

[x] - key: {{ rs.key }} value: {{ rs.value }}</br>

{% endif %}
