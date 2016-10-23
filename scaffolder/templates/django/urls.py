from __future__ import unicode_literals

from django.conf.urls import include, url

from .views import {% for model in app.models %}{{ model.name | capitalize }}IndexView{% if not loop.last %}, {% endif %}{% endfor %}
from .views import {% for model in app.models %}{{ model.name | capitalize }}DetailView{% if not loop.last %}, {% endif %}{% endfor %}

app_name = '{{ app.name }}'
urlpatterns = [
    {% for model in app.models %}
    url(r'^{{ model.name | lower }}s/$', {{model.name}}IndexView.as_view(), name='{{ model.name | lower }}s-list'),
    url(r'^{{ model.name | lower }}s/(?P<pk>[0-9]+)/$',
        {{ model.name }}DetailView.as_view(), name='{{ model.name | lower }}s-detail'),
    {% endfor %}
]
