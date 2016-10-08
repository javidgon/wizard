from __future__ import unicode_literals

from django.contrib import admin

from .models import {% for model in models %}{{ model.name }}{% if not loop.last %}, {% endif %}{% endfor %}


{% for model in models %}admin.site.register({{ model.name }})
{% endfor %}