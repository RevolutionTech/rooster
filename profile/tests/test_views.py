import datetime
from http import HTTPStatus
from unittest import mock

import pytz
from django.test import TestCase

from rooster.factories import UserFactory


def serialize_datetime(dt):
    return dt.isoformat().replace("+00:00", "Z")


class TestDashboardView(TestCase):
    @mock.patch(
        "profile.views.GithubAPI.get_events_for_dashboard",
        return_value=[
            {
                "created_at": datetime.datetime(2019, 3, 1, tzinfo=pytz.utc),
                "subheader": "PR Reviews",
                "repo": {
                    "name": "jsmith/alpha",
                    "url": "https://github.com/repos/jsmith/alpha",
                },
                "pull_request": {
                    "title": "Finish beta",
                    "url": "https://github.com/jsmith/alpha/pulls/100",
                    "author": "Mary Doe",
                },
            },
            {
                "created_at": datetime.datetime(2019, 3, 1, tzinfo=pytz.utc),
                "subheader": "Pull Requests",
                "repo": {
                    "name": "jsmith/foo",
                    "url": "https://github.com/repos/jsmith/foo",
                },
                "pull_request": {
                    "title": "Add baz",
                    "url": "https://github.com/jsmith/foo/pulls/101",
                    "author": "John Smith",
                },
            },
            {
                "created_at": datetime.datetime(2019, 1, 1, tzinfo=pytz.utc),
                "subheader": "Pull Requests",
                "repo": {
                    "name": "jsmith/foo",
                    "url": "https://github.com/repos/jsmith/foo",
                },
                "pull_request": {
                    "title": "Add bar",
                    "url": "https://github.com/jsmith/foo/pulls/100",
                    "author": "John Smith",
                },
            },
        ],
    )
    @mock.patch("profile.views.GithubAPI.__init__", return_value=None)
    @mock.patch("profile.views.JiraAPI.get_in_progress_tickets")
    @mock.patch("jiraapi.api.JIRA.__init__", return_value=None)
    def test_get_dashboard(
        self,
        mock_jira_init,
        mock_get_tickets,
        mock_githubapi_init,
        mock_get_events_for_dashboard,
    ):
        user = UserFactory()

        mock_get_tickets.return_value = [
            {
                "issue_key": "FOO-100",
                "summary": "Add bar to Foo",
                "url": f"{user.usersettings.jira_server_url}/browse/FOO-100",
            }
        ]

        self.client.force_login(user)

        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        mock_jira_init.assert_called_once()
        mock_get_tickets.assert_called_once()
        mock_githubapi_init.assert_called_once_with(user)
        mock_get_events_for_dashboard.assert_called_once()


class TestSettingsView(TestCase):
    def test_get_settings(self):
        user = UserFactory()
        self.client.force_login(user)

        response = self.client.get("/settings")
        self.assertEqual(response.status_code, HTTPStatus.OK)


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
