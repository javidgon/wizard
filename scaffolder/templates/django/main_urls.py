from __future__ import unicode_literals

"""maintainme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from .views import index, login, logout, create_user


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^create_user/$', create_user),

    {% if frontend %}
    # APIS
    {% for app in apps %}url(r'^api/v1/{{ app.name | lower }}/', include('{{ app.name | lower }}.api_urls')),
    {% endfor %}
    url(r'^.*$', index),
    {% else %}
    # VIEWS
    {% for app in apps %}url(r'{{ app.name | lower }}/', include('{{ app.name | lower }}.urls')),
    {% endfor %}
    url(r'^$', index),
    {% endif %}
    ]
