from django.urls import path

from github.views import ProfileView

urlpatterns = [path("", ProfileView.as_view())]
