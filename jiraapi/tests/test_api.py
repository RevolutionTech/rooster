from unittest import mock

from django.test import TestCase

from jiraapi.api import JiraAPI
from rooster.factories import UserFactory


class TestGetInProgressTickets(TestCase):
    @mock.patch("jiraapi.api.JIRA.search_issues")
    @mock.patch("jiraapi.api.JIRA.__init__", return_value=None)
    def test_get_in_progress_tickets(self, mock_jira_init, mock_search_issues):
        user = UserFactory()
        user_settings = user.usersettings

        jira_server_url = user.usersettings.jira_server_url
        mock_search_issues.return_value = [
            mock.Mock(
                key="FOO-101",
                fields=mock.Mock(summary="Create parent class for bar"),
                permalink=lambda: f"{jira_server_url}/browse/FOO-101",
            ),
            mock.Mock(
                key="FOO-100",
                fields=mock.Mock(summary="Add bar to Foo"),
                permalink=lambda: f"{jira_server_url}/browse/FOO-100",
            ),
        ]

        api = JiraAPI(user)
        mock_jira_init.assert_called_once_with(
            {"server": user_settings.jira_server_url},
            basic_auth=(user_settings.jira_email, user_settings.jira_api_key),
        )

        expected = [
            {
                "issue_key": "FOO-101",
                "summary": "Create parent class for bar",
                "url": f"{jira_server_url}/browse/FOO-101",
            },
            {
                "issue_key": "FOO-100",
                "summary": "Add bar to Foo",
                "url": f"{jira_server_url}/browse/FOO-100",
            },
        ]

        actual = api.get_in_progress_tickets()
        self.assertEqual(actual, expected)
