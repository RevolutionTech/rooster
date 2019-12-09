from unittest import mock

from django.test import TestCase

from githubapi.api import GithubAPI
from rooster.factories import UserFactory


class TestGetPullRequests(TestCase):
    @mock.patch("githubapi.api.Github.get_user")
    def test_get_pull_requests(self, mock_get_user):
        project_name = "Project Name"
        pr_title = "PR Title"
        mock_project = mock.Mock()
        mock_project.name = project_name
        mock_get_user.side_effect = [
            mock.Mock(login="jsmith"),
            mock.Mock(
                get_events=lambda: [
                    mock.Mock(
                        type="PullRequestEvent",
                        repo=mock_project,
                        payload={"pull_request": {"title": pr_title}},
                    ),
                    mock.Mock(type="IrrelevantEvent"),
                ]
            ),
        ]

        user = UserFactory()
        api = GithubAPI(user)

        expected_list = [{"repo_name": project_name, "title": pr_title}]

        pull_requests = api.get_pull_requests()
        for actual, expected in zip(pull_requests, expected_list):
            self.assertEqual(actual, expected)
