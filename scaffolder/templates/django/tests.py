from __future__ import unicode_literals

import json

from django.test import TestCase, Client
from django.urls import reverse
from autofixture import AutoFixture

from .models import {% for model in app.models %}{{ model.name }}{% if not loop.last %}, {% endif %}{% endfor %}
from .api import {% for model in app.models %}{{ model.name }}Api{% if not loop.last %}, {% endif %}{% endfor %}

{% for model in app.models %}
class {{model.name}}ApiTest(TestCase):
    def setUp(self):
        fixture = AutoFixture({{ model.name }})
        self.entries = fixture.create(10)


    def test_get_list_elements(self):
        c = Client()
        resp = c.get(reverse('{{ app.name}}:{{ model.name | lower }}s-list'))

        expected = [entry.to_dict() for entry in self.entries]
        import pdb; pdb.set_trace()
        self.assertEqual(int(resp.status_code), 200)
        self.assertEqual(json.load(resp.content), expected)

{% endfor %}