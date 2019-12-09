import datetime
from unittest import mock

import pytz
from django.test import TestCase

from githubapi.api import GithubAPI
from rooster.factories import UserFactory


class TestGetEvents(TestCase):
    @mock.patch("githubapi.api.Github.get_user")
    def test_get_events(self, mock_get_user):
        pr_created_dt = datetime.datetime(2019, 1, 1, tzinfo=pytz.utc)
        project_name = "Project Name"
        pr_title = "PR Title"
        other_pr_title = "Other PR"
        mock_project = mock.Mock()
        mock_project.name = project_name
        mock_get_user.side_effect = [
            mock.Mock(login="jsmith"),
            mock.Mock(
                get_events=lambda: [
                    mock.Mock(
                        created_at=pr_created_dt + datetime.timedelta(hours=2),
                        type="PullRequestReviewCommentEvent",
                        repo=mock_project,
                        payload={"pull_request": {"title": other_pr_title}},
                    ),
                    mock.Mock(type="IrrelevantEvent"),
                    mock.Mock(
                        created_at=pr_created_dt,
                        type="PullRequestEvent",
                        repo=mock_project,
                        payload={"pull_request": {"title": pr_title}},
                    ),
                ]
            ),
        ]

        user = UserFactory()
        api = GithubAPI(user)

        expected_list = [
            {
                "created_at": pr_created_dt + datetime.timedelta(hours=2),
                "subheader": "PR Reviews",
                "repo_name": project_name,
                "title": other_pr_title,
            },
            {
                "created_at": pr_created_dt,
                "subheader": "Pull Requests",
                "repo_name": project_name,
                "title": pr_title,
            },
        ]

        events = api.get_events()
        for actual, expected in zip(events, expected_list):
            self.assertEqual(actual, expected)
