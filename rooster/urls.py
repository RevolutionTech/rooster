from django.conf.urls import url
from django.urls import path, include

from github.views import ProfileView

urlpatterns = [
    url("", include("social_django.urls", namespace="social")),
    path("", ProfileView.as_view()),
]
