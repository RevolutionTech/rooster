from profile.models import UserSettings

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from githubapi.api import GithubAPI
from jiraapi.api import JiraAPI


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
