import datetime
from http import HTTPStatus
from unittest import mock

import pytz
from django.test import TestCase

from rooster.factories import UserFactory


class TestProfileView(TestCase):
    @mock.patch(
        "profile.views.GithubAPI.get_events",
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
    def test_get_profile(self, mock_githubapi_init, mock_get_events):
        user = UserFactory()
        self.client.force_login(user)

        response = self.client.get("/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        mock_githubapi_init.assert_called_once_with(user)
        mock_get_events.assert_called_once()
