from django.conf.urls import url
from django.urls import path, include

from profile.views import ProfileView

urlpatterns = [
    url("", include("social_django.urls", namespace="social")),
    url(r"^tz_detect/", include("tz_detect.urls")),
    path("", ProfileView.as_view()),
]
