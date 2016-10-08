from django.db import models
{% for model in models %}

class {{model.name}}(models.Model):
    {% for field in model.fields %}{{ field}} = # WRITE FIELD DESCRIPTION HERE,
    {% endfor %}
    def __str__(self):
        return {{ model.str }}

    def to_dict(self):
        return {
            {% for field in model.fields %}'{{field}}': self.{{field}},
            {% endfor %}
        }
{% endfor %}