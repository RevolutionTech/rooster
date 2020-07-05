from profile.models import UserSettings

from django.contrib.auth.models import User
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name",)

    full_name = CharField(source="get_full_name")


class UserSettingsSerializer(ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ("jira_server_url", "jira_email", "jira_api_key")

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data["user"] = self.context["request"].user
        return validated_data
