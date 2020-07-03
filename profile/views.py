from profile.models import UserSettings

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from githubapi.api import GithubAPI
from jiraapi.api import JiraAPI


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        jira_api = JiraAPI(user)
        github_api = GithubAPI(user)
        context.update(
            {
                "jira_valid_credentials": jira_api.valid_credentials,
                "tickets": jira_api.get_in_progress_tickets(),
                "events": github_api.get_events_for_dashboard(),
            }
        )

        return context


class SettingsView(LoginRequiredMixin, UpdateView):
    template_name = "settings.html"
    model = UserSettings
    fields = ["jira_server_url", "jira_email", "jira_api_key"]
    success_url = reverse_lazy("dashboard")

    def get_object(self):
        user_settings, _ = UserSettings.objects.get_or_create(user=self.request.user)
        return user_settings


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {"full_name": user.get_full_name()}
        return Response(data, status=status.HTTP_200_OK)


class ActivitiesInProgressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        jira_api = JiraAPI(user)
        data = {"jira_tickets": jira_api.get_in_progress_tickets()}
        return Response(data, status=status.HTTP_200_OK)


class ActivityHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        github_api = GithubAPI(user)
        return Response(github_api.get_events(), status=status.HTTP_200_OK)


class SettingsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_response_from_user_settings(user_settings):
        data = {
            "jira_server_url": user_settings.jira_server_url,
            "jira_email": user_settings.jira_email,
            "jira_api_key": user_settings.jira_api_key,
        }
        return Response(data, status=status.HTTP_200_OK)

    def get(self, request):
        user_settings, _ = UserSettings.objects.get_or_create(user=request.user)
        return self.get_response_from_user_settings(user_settings)

    def put(self, request):
        user_settings, _ = UserSettings.objects.update_or_create(
            user=request.user, defaults=request.data
        )
        return self.get_response_from_user_settings(user_settings)
