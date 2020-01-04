from github import Github
from social_django.utils import load_strategy

from githubapi.events import event_type_from_github_event


class GithubAPI:
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
            event_type = event_type_from_github_event(github_event)
            if event_type:
                repo = github_event.repo
                payload = github_event.payload
                pull_request = payload["pull_request"]
                pr_title = pull_request["title"]

                all_events.append(
                    {
                        "created_at": github_event.created_at,
                        "subheader": event_type.subheader,
                        "repo": {"name": repo.name, "url": repo.html_url},
                        "pull_request": {"title": pr_title},
                    }
                )

        sorted_events = sorted(
            all_events,
            key=lambda event: (event["created_at"], event["subheader"].lower()),
            reverse=True,
        )
        return sorted_events
