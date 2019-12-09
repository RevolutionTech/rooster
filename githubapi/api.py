from github import Github
from social_django.utils import load_strategy


class GithubAPI:
    def __init__(self, user):
        strategy = load_strategy()
        user_social_auth = user.social_auth.get()
        access_token = user_social_auth.get_access_token(strategy)
        self.api = Github(access_token)
        github_authenticated_user = self.api.get_user()
        self.github_named_user = self.api.get_user(github_authenticated_user.login)

    def get_pull_requests(self):
        for event in self.github_named_user.get_events():
            if event.type == "PullRequestEvent":
                payload = event.payload
                pr_title = payload["pull_request"]["title"]

                yield {"repo_name": event.repo.name, "title": pr_title}
