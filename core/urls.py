from __future__ import unicode_literals

from django.conf.urls import include, url

from .api import urls

urlpatterns = [url("api/", include(urls))]
