from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse

import json

{% for model in app.models %}
from .models import {{ model.name }}
{% endfor %}

{% for model in app.models %}class {{model.name}}Api(View):
    def get(self, request, {{ model.name | lower }}_id):
        if {{ model.name | lower }}_id:
            {{ model.name | lower }} = get_object_or_404({{model.name}}, pk={{ model.name | lower }}_id)
            return JsonResponse({{ model.name | lower }}.to_dict())
        {{model.name | lower}}s = {{ model.name }}.objects.all()
        resp = [{{model.name | lower}}.to_dict for {{model.name | lower}} in {{model.name | lower}}s]
        return JsonResponse(resp)

    def post(self, request, {{ model.name | lower }}_id):
        if not {{ model.name | lower }}_id:
            return HttpResponseBadRequest()

        {{model.name | lower}} = {{ model.name }}.objects.create(
            {% for field in model.fields %}{{ field }}=request.POST.get('{{ field }}'),
            {% endfor %}
        )
        return JsonResponse({{model.name | lower}}.to_dict())

    def put(self, request, {{model.name | lower}}_id):
        if not {{model.name | lower}}_id:
            return HttpResponseBadRequest()

        {{model.name | lower}} = get_object_or_404({{model.name}}, pk={{model.name | lower}}_id)
        {{model.name | lower}} = {{model.name}}.objects.update(
            {% for field in model.fields %}{{field}}=request.POST.get('{{ field }}'),
            {% endfor %}
        )
        return JsonResponse({{ model.name | lower }}.to_dict())

    def delete(self, request, {{model.name | lower}}_id):
        if not {{model.name | lower}}_id:
            return HttpResponseBadRequest()

        {{model.name | lower}} = get_object_or_404({{model.name}}, pk={{model.name | lower}}_id)
        {{model.name}}.objects.delete(id={{model.name | lower}}_id)
        return HttpResponse(status_code=200)


{% endfor %}