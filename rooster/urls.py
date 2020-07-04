from profile.views import (
    ActivitiesInProgressAPIView,
    ActivityHistoryAPIView,
    SettingsAPIView,
    UserAPIView,
)

from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import include, path

urlpatterns = [
    url("", include("social_django.urls", namespace="social")),
    url("logout/", LogoutView.as_view(), name="auth_logout"),
    path("api/user/", UserAPIView.as_view(), name="user"),
    path(
        "api/activities/in-progress/",
        ActivitiesInProgressAPIView.as_view(),
        name="activities_in_progress",
    ),
    path(
        "api/activities/history/",
        ActivityHistoryAPIView.as_view(),
        name="activities_history",
    ),
    path("api/settings/", SettingsAPIView.as_view(), name="settings"),
]
