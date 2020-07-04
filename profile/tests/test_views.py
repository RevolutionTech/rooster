import datetime
from http import HTTPStatus
from profile.models import UserSettings
from profile.tests.factories import UserSettingsFactory
from unittest import mock

import pytz
from django.test import TestCase

from rooster.factories import UserFactory


def serialize_datetime(dt):
    return dt.isoformat().replace("+00:00", "Z")


class TestUserAPIView(TestCase):
    def test_get_user(self):
        user = UserFactory()

        self.client.force_login(user)

        response = self.client.get("/api/user/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json(), {"full_name": user.get_full_name()})


class TestActivitiesInProgressAPIView(TestCase):
    @mock.patch("profile.views.JiraAPI.get_in_progress_tickets")
    @mock.patch("jiraapi.api.JIRA.__init__", return_value=None)
    def test_get_activities_in_progress(self, mock_jira_init, mock_get_tickets):
        user = UserFactory()

        jira_tickets = [
            {
                "issue_key": "FOO-100",
                "summary": "Add bar to Foo",
                "url": f"{user.usersettings.jira_server_url}/browse/FOO-100",
            }
        ]
        mock_get_tickets.return_value = jira_tickets

        self.client.force_login(user)

        response = self.client.get("/api/activities/in-progress/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.json(), {"jira_tickets": jira_tickets},
        )

        mock_jira_init.assert_called_once()
        mock_get_tickets.assert_called_once()


class TestActivityHistoryAPIView(TestCase):
    @mock.patch("profile.views.GithubAPI.get_events",)
    @mock.patch("profile.views.GithubAPI.__init__", return_value=None)
    def test_get_activity_history(self, mock_githubapi_init, mock_get_events):
        events = [
            {
                "created_at": datetime.datetime(2019, 3, 1, 14, 0, 0, tzinfo=pytz.utc),
                "activity_type": "PR Reviews",
                "pull_request": {
                    "repo": {
                        "name": "jsmith/alpha",
                        "url": "https://github.com/repos/jsmith/alpha",
                    },
                    "title": "Finish beta",
                    "url": "https://github.com/jsmith/alpha/pulls/100",
                    "author": "Mary Doe",
                },
            },
            {
                "created_at": datetime.datetime(2019, 3, 1, 11, 0, 0, tzinfo=pytz.utc),
                "activity_type": "Pull Requests",
                "pull_request": {
                    "repo": {
                        "name": "jsmith/foo",
                        "url": "https://github.com/repos/jsmith/foo",
                    },
                    "title": "Add baz",
                    "url": "https://github.com/jsmith/foo/pulls/101",
                    "author": "John Smith",
                },
            },
            {
                "created_at": datetime.datetime(2019, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
                "activity_type": "Pull Requests",
                "pull_request": {
                    "repo": {
                        "name": "jsmith/foo",
                        "url": "https://github.com/repos/jsmith/foo",
                    },
                    "title": "Add bar",
                    "url": "https://github.com/jsmith/foo/pulls/100",
                    "author": "John Smith",
                },
            },
        ]
        mock_get_events.return_value = events

        user = UserFactory()
        self.client.force_login(user)

        response = self.client.get("/api/activities/history/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.json(),
            [
                {**event, "created_at": serialize_datetime(event["created_at"])}
                for event in events
            ],
        )

        mock_githubapi_init.assert_called_once_with(user)
        mock_get_events.assert_called_once()


class TestSettingsAPIView(TestCase):
    JIRA_SETTINGS = {"jira_server_url", "jira_email", "jira_api_key"}

    def test_get_settings(self):
        user = UserFactory()
        self.client.force_login(user)

        response = self.client.get("/api/settings/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.json(),
            {
                setting: getattr(user.usersettings, setting)
                for setting in self.JIRA_SETTINGS
            },
        )

    def test_create_empty_settings(self):
        user = UserFactory()
        user.usersettings.delete()

        self.client.force_login(user)

        response = self.client.get("/api/settings/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.json(), {setting: "" for setting in self.JIRA_SETTINGS},
        )

        # Validate that user settings were created
        self.assertTrue(UserSettings.objects.filter(user=user).exists())

    def test_put_settings(self):
        user = UserFactory()
        settings_data = UserSettingsFactory.stub()
        self.client.force_login(user)

        request_data = {
            setting: getattr(settings_data, setting) for setting in self.JIRA_SETTINGS
        }
        response = self.client.put(
            "/api/settings/", request_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json(), request_data)

        # Validate that user settings were updated
        user.usersettings.refresh_from_db()
        for setting in self.JIRA_SETTINGS:
            self.assertEqual(
                getattr(user.usersettings, setting), getattr(settings_data, setting)
            )
