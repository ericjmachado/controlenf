from __future__ import unicode_literals

from django.conf.urls import url, include

from .v1 import urls

urlpatterns = [url("v1/", include(urls))]
