import datetime
from unittest import mock

import pytz
from django.test import TestCase

from githubapi.api import GithubAPI
from rooster.factories import UserFactory


@mock.patch("githubapi.api.Github.get_user")
class TestGetEvents(TestCase):
    def test_get_events(self, mock_get_user):
        pr_created_dt = datetime.datetime(2020, 1, 1, tzinfo=pytz.utc)
        project_name = "Project Name"
        pr_title = "PR Title"
        other_pr_title = "Other PR"

        user = UserFactory()

        repo_url = f"https://github.com/repos/{user.username}/project-name"
        mock_project = mock.Mock(html_url=repo_url)
        mock_project.name = project_name
        mock_get_user.side_effect = [
            mock.Mock(login="jsmith"),
            mock.Mock(
                get_events=lambda: [
                    mock.Mock(
                        created_at=pr_created_dt + datetime.timedelta(hours=2),
                        type="PullRequestReviewCommentEvent",
                        repo=mock_project,
                        payload={
                            "action": "created",
                            "pull_request": {
                                "id": 101,
                                "title": other_pr_title,
                                "html_url": f"{repo_url}/pulls/101",
                            },
                        },
                    ),
                    mock.Mock(type="IrrelevantEvent"),
                    mock.Mock(
                        created_at=pr_created_dt,
                        type="PullRequestEvent",
                        repo=mock_project,
                        payload={
                            "action": "opened",
                            "pull_request": {
                                "id": 100,
                                "title": pr_title,
                                "html_url": f"{repo_url}/pulls/100",
                            },
                        },
                    ),
                ]
            ),
        ]

        api = GithubAPI(user)

        expected_list = [
            {
                "created_at": pr_created_dt + datetime.timedelta(hours=2),
                "subheader": "PR Reviews",
                "repo": {"name": project_name, "url": repo_url},
                "pull_request": {
                    "title": other_pr_title,
                    "url": f"{repo_url}/pulls/101",
                },
            },
            {
                "created_at": pr_created_dt,
                "subheader": "Pull Requests",
                "repo": {"name": project_name, "url": repo_url},
                "pull_request": {"title": pr_title, "url": f"{repo_url}/pulls/100"},
            },
        ]

        events = api.get_events()
        for actual, expected in zip(events, expected_list):
            self.assertEqual(actual, expected)

    def test_no_duplicates(self, mock_get_user):
        pr_created_dt = datetime.datetime(2020, 1, 1, 12, 0, 0, tzinfo=pytz.utc)
        project_name = "Project Name"
        pr_title = "PR Title"

        user = UserFactory()

        repo_url = f"https://github.com/repos/{user.username}/project-name"
        mock_project = mock.Mock(html_url=repo_url)
        mock_project.name = project_name
        mock_get_user.side_effect = [
            mock.Mock(login="jsmith"),
            mock.Mock(
                get_events=lambda: [
                    mock.Mock(
                        created_at=pr_created_dt,
                        type="PullRequestReviewCommentEvent",
                        repo=mock_project,
                        payload={
                            "action": "created",
                            "pull_request": {
                                "id": 100,
                                "title": pr_title,
                                "html_url": f"{repo_url}/pulls/100",
                            },
                        },
                    ),
                    mock.Mock(
                        created_at=pr_created_dt - datetime.timedelta(hours=2),
                        type="PullRequestReviewCommentEvent",
                        repo=mock_project,
                        payload={
                            "action": "created",
                            "pull_request": {
                                "id": 100,
                                "title": pr_title,
                                "html_url": f"{repo_url}/pulls/100",
                            },
                        },
                    ),
                ]
            ),
        ]

        api = GithubAPI(user)

        expected_list = [
            {
                "created_at": pr_created_dt,
                "subheader": "PR Reviews",
                "repo": {"name": project_name, "url": repo_url},
                "pull_request": {"title": pr_title, "url": f"{repo_url}/pulls/100"},
            }
        ]

        events = api.get_events()
        for actual, expected in zip(events, expected_list):
            self.assertEqual(actual, expected)
