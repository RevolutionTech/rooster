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
                "repo_name": "jsmith/alpha",
                "title": "Finish beta",
            },
            {
                "created_at": datetime.datetime(2019, 3, 1, tzinfo=pytz.utc),
                "subheader": "Pull Requests",
                "repo_name": "jsmith/foo",
                "title": "Add baz",
            },
            {
                "created_at": datetime.datetime(2019, 1, 1, tzinfo=pytz.utc),
                "subheader": "Pull Requests",
                "repo_name": "jsmith/foo",
                "title": "Add bar",
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
