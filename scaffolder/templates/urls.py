from __future__ import unicode_literals

from django.conf.urls import include, url

from .api import {% for model in app.models %}{{ model.name | capitalize }}Api{% if not loop.last %}, {% endif %}{% endfor %}

app_name = '{{ app.name }}'
urlpatterns = [
    {% for model in app.models %}
    url(r'^{{ model.name | lower }}s/$', {{model.name}}Api.as_view(), name='{{ model.name | lower }}s-list'),
    url(r'^{{ model.name | lower }}s/(?P<{{model.name | lower }}_id>[0-9]+)/$',
        {{ model.name }}Api.as_view(), name='{{ model.name | lower }}s-detail'),
    {% endfor %}
]
