from github import Github
from social_django.utils import load_strategy


class GithubAPI:
    SUBHEADER_FROM_EVENT_TYPE = {
        "PullRequestEvent": "Pull Requests",
        "PullRequestReviewCommentEvent": "PR Reviews",
    }

    def __init__(self, user):
        strategy = load_strategy()
        user_social_auth = user.social_auth.get()
        access_token = user_social_auth.get_access_token(strategy)
        self.api = Github(access_token)
        github_authenticated_user = self.api.get_user()
        self.github_named_user = self.api.get_user(github_authenticated_user.login)

    def get_events(self):
        all_events = []

        for github_event in self.github_named_user.get_events():
            if github_event.type in self.SUBHEADER_FROM_EVENT_TYPE:
                payload = github_event.payload
                pr_title = payload["pull_request"]["title"]

                all_events.append(
                    {
                        "created_at": github_event.created_at,
                        "subheader": self.SUBHEADER_FROM_EVENT_TYPE[github_event.type],
                        "repo_name": github_event.repo.name,
                        "title": pr_title,
                    }
                )

        sorted_events = sorted(
            all_events,
            key=lambda event: (event["created_at"], event["subheader"].lower()),
            reverse=True,
        )
        return sorted_events
