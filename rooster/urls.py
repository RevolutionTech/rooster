from profile.views import (
    ActivitiesInProgressAPIView,
    ActivityHistoryAPIView,
    SettingsAPIView,
    UserAPIView,
)

from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from django.views.decorators.cache import never_cache

urlpatterns = [
    url("", include("social_django.urls", namespace="social")),
    url("logout/", LogoutView.as_view(), name="auth_logout"),
    path("api/user/", never_cache(UserAPIView.as_view()), name="user"),
    path(
        "api/activities/in-progress/",
        never_cache(ActivitiesInProgressAPIView.as_view()),
        name="activities_in_progress",
    ),
    path(
        "api/activities/history/",
        never_cache(ActivityHistoryAPIView.as_view()),
        name="activities_history",
    ),
    path("api/settings/", never_cache(SettingsAPIView.as_view()), name="settings"),
]
