from profile.serializers import UserSerializer, UserSettingsSerializer
from profile.tests.factories import UserSettingsFactory

from django.test import RequestFactory, TestCase

from rooster.factories import UserFactory


class TestUserSerializer(TestCase):
    def test_serialize(self):
        user = UserFactory()

        serialized_data = UserSerializer(user).data
        self.assertEqual(serialized_data, {"full_name": user.get_full_name()})


class TestUserSettingsSerializer(TestCase):
    def test_serialize(self):
        user = UserFactory()

        serialized_data = UserSettingsSerializer(user.usersettings).data
        self.assertEqual(
            serialized_data,
            {
                "jira_server_url": user.usersettings.jira_server_url,
                "jira_email": user.usersettings.jira_email,
                "jira_api_key": user.usersettings.jira_api_key,
            },
        )

    def test_deserialize(self):
        user = UserFactory()

        rf = RequestFactory()
        request = rf.get("/")
        request.user = user

        user.usersettings.delete()
        user_settings_data = UserSettingsFactory.build()

        data = {
            "jira_server_url": user_settings_data.jira_server_url,
            "jira_email": user_settings_data.jira_email,
            "jira_api_key": user_settings_data.jira_api_key,
        }

        serializer = UserSettingsSerializer(data=data, context={"request": request})
        self.assertTrue(serializer.is_valid())
        user_settings = serializer.save()

        self.assertEqual(
            user_settings.jira_server_url, user_settings_data.jira_server_url
        )
        self.assertEqual(user_settings.jira_email, user_settings_data.jira_email)
        self.assertEqual(user_settings.jira_api_key, user_settings_data.jira_api_key)
