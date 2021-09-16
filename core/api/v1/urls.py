from __future__ import unicode_literals

from django.conf.urls import url, include
from django.urls import path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()


urlpatterns = [
    url("", include(router.urls)),
    # path("login/", views.LoginView.as_view()),
    # path("refresh-token/", views.RefreshView.as_view()),
    # path("token-verify/", views.VerifyTokenView.as_view()),
]
