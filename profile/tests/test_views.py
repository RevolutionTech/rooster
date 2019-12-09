from http import HTTPStatus
from unittest import mock

from django.test import TestCase

from rooster.factories import UserFactory


class TestProfileView(TestCase):
    @mock.patch(
        "profile.views.GithubAPI.get_pull_requests",
        return_value=[
            {"repo_name": "jsmith/foo", "title": "Add bar"},
            {"repo_name": "jsmith/foo", "title": "Add baz"},
        ],
    )
    @mock.patch("profile.views.GithubAPI.__init__", return_value=None)
    def test_get_profile(self, mock_githubapi_init, mock_get_pull_requests):
        user = UserFactory()
        self.client.force_login(user)

        response = self.client.get("/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        mock_githubapi_init.assert_called_once_with(user)
        mock_get_pull_requests.assert_called_once()
