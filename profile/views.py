import logging
from profile.models import UserSettings
from profile.serializers import UserSerializer, UserSettingsSerializer

from rest_framework import status
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from githubapi.api import GithubAPI
from jiraapi.api import JiraAPI

logger = logging.getLogger(__name__)


class IsAuthenticatedWLogging(IsAuthenticated):
    def has_permission(self, request, view):
        result = super().has_permission(request, view)
        if not result:
            logger.info(
                "%s: user: %s; cookies: %s", request.path, request.user, request.COOKIES
            )
        return result


class UserAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedWLogging]

    def get_object(self):
        return self.request.user


class ActivitiesInProgressAPIView(APIView):
    permission_classes = [IsAuthenticatedWLogging]

    def get(self, request):
        user = request.user
        jira_api = JiraAPI(user)
        data = {"jira_tickets": jira_api.get_in_progress_tickets()}
        return Response(data, status=status.HTTP_200_OK)


class ActivityHistoryAPIView(APIView):
    permission_classes = [IsAuthenticatedWLogging]

    def get(self, request):
        user = request.user
        github_api = GithubAPI(user)
        return Response(github_api.get_events(), status=status.HTTP_200_OK)


class SettingsAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSettingsSerializer
    permission_classes = [IsAuthenticatedWLogging]

    def get_object(self):
        user_settings, _ = UserSettings.objects.get_or_create(user=self.request.user)
        return user_settings
