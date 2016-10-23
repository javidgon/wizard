from __future__ import unicode_literals

from django.views import generic

from .models import {% for model in app.models %}{{ model.name }}{% if not loop.last %}, {% endif %}{% endfor %}


{% for model in app.models %}class {{ model.name }}IndexView(generic.ListView):
    model = {{ model.name }}
    template_name = '{{ model.name | lower }}s/index.html'

class {{ model.name }}DetailView(generic.DetailView):
    model = {{ model.name }}
    template_name = '{{ model.name | lower }}s/detail.html'

{% endfor %}
