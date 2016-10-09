from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse

from .models import {% for model in app.models %}{{ model.name }}{% if not loop.last %}, {% endif %}{% endfor %}


{% for model in app.models %}class {{ model.name }}Api(View):
    def get(self, request, {{ model.name | lower }}_id=None, *args, **kwargs):
        if {{ model.name | lower }}_id:
            {{ model.name | lower }}, _ = get_object_or_404({{ model.name }}, pk={{ model.name | lower }}_id)
            return JsonResponse({{ model.name | lower }}.to_dict())
        {{model.name | lower}}s = {{ model.name }}.objects.all()
        resp = [{{ model.name | lower }}.to_dict for {{ model.name | lower }} in {{ model.name | lower }}s]
        return JsonResponse(resp, safe=False)

    def post(self, request, {{ model.name | lower }}_id=None, *args, **kwargs):
        if not {{ model.name | lower }}_id:
            return HttpResponseBadRequest()

        {{ model.name | lower }} = {{ model.name }}.objects.create(
            {% for field in model.fields %}{% for name, props in field.iteritems() %}{{ name }}=request.POST.get('{{ name }}'),{% endfor %}
            {% endfor %})
        return JsonResponse({{ model.name | lower }}.to_dict(), safe=False)

    def put(self, request, {{ model.name | lower }}_id=None, *args, **kwargs):
        if not {{ model.name | lower }}_id:
            return HttpResponseBadRequest()

        {{ model.name | lower }}, _ = get_object_or_404({{model.name}}, pk={{ model.name | lower }}_id)
        {{ model.name | lower}} = {{ model.name }}.objects.update(
            {% for field in model .fields %}{% for name, props in field.iteritems() %}{{ name }}=request.POST.get('{{ name }}'),{% endfor %}
            {% endfor %})
        return JsonResponse({{ model.name | lower }}.to_dict(), safe=False)

    def delete(self, request, {{ model.name | lower }}_id=None, *args, **kwargs):
        if not {{ model.name | lower }}_id:
            return HttpResponseBadRequest()

        {{ model.name | lower }}, _ = get_object_or_404({{ model.name }}, pk={{ model.name | lower }}_id)
        {{ model.name }}.objects.delete(id={{ model.name | lower }}_id)
        return HttpResponse(status_code=200)


{% endfor %}