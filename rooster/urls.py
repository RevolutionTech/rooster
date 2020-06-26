from profile.views import (
    ActivitiesInProgressAPIView,
    ActivityHistoryAPIView,
    DashboardView,
    SettingsView,
    UserAPIView,
)

from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import include, path

urlpatterns = [
    url("", include("social_django.urls", namespace="social")),
    url("logout/", LogoutView.as_view(), name="auth_logout"),
    url(r"^tz_detect/", include("tz_detect.urls")),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("settings", SettingsView.as_view(), name="settings"),
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
]
