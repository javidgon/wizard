from django.conf.urls import include, url

{% for model in app.models %}from .api import {{model.name}}Api
{% endfor %}

app_name = '{{ app.name }}'
urlpatterns = [
    {% for model in app.models %}
    url(r'^{{ model.name | lower }}s/$', {{model.name}}Api.as_view(), name='{{ model.name | lower }}s-list'),
    url(r'^{{ model.name | lower }}s/(?P<{{model.name | lower }}_id>[0-9]+)/$',
        {{ model.name }}Api.as_view(), name='{{ model.name | lower }}s-detail'),
    {% endfor %}
]
