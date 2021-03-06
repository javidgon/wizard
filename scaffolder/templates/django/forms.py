from __future__ import unicode_literals

from django.forms import ModelForm

from .models import {% for model in app.models %}{{ model.name }}{% if not loop.last %}, {% endif %}{% endfor %}{% for model in app.models %}


class {{ model.name }}Form(ModelForm):
    class Meta:
        model = {{ model.name }}
        fields = '__all__'

{% endfor %}
