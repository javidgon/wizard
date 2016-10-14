from __future__ import unicode_literals

# This is always imported as Models might use it.
from django.contrib.auth.models import User
from {{ project.name }}.models import UserToken
from django.db import models{% for model in app.models %}


class {{model.name}}(models.Model):
    app_label = '{{ app.name }}'

    {% for field in model.fields %}{% for name, props in field.iteritems() %}{{ name }} = {% if 'char' in props %}models.CharField({% endif %}{% if 'int' in props %}models.IntegerField({% endif %}{% if 'float' in props %}models.FloatField({% endif %}{% if 'text' in props %}models.TextField({% endif %}{% if 'url' in props %}models.UrlField({% endif %}{% if 'date' in props %}models.DateField({% endif %}{% if 'datetime' in props %}models.DateTimeField({% endif %}{% if 'email' in props %}models.EmailField({% endif %}{% if 'boolean' in props %}models.BooleanField({% endif %}{% if 'foreign' in props %}models.ForeignKey({{ name | capitalize }}, {% endif %}{% if 'manytomany' in props %}models.ManyToManyField({{ name|capitalize }}{% endif %}{% if 'unique' in props %}unique=True,{% endif %}{% if 'notunique' in props %}unique=False,{% endif %}{% if 'blank' in props %}blank=True,{% endif %}{% if 'notblank' in props %}blank=False,{% endif %}{% if 'null' in props %}null=True,{% endif %}{% if 'notnull' in props %}null=False,{% endif %}{% if 'auto_now' in props %}auto_now=True,{% endif %}{% if 'auto_now_add' in props %}auto_now_add=True,{% endif %}), {% endfor %}
    {% endfor %}
    def __unicode__(self):
        return '{% for field in model.unicode %}{}{% if not loop.last %}, {% endif %}{% endfor %}'.format({% for field in model.unicode %}self.{{ field }}{% if not loop.last %}, {% endif %}{% endfor %})

    def to_dict(self):
        return {
            {% for field in model.fields %}{% for name, props in field.iteritems() %}'{{ name }}': self.{{ name }},{% endfor %}
            {% endfor %}}{% endfor %}
