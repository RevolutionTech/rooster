from github import Github
from social_django.utils import load_strategy

from githubapi.events import event_from_github_event


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
            event = event_from_github_event(github_event)
            if event:
                all_events.append(event.get_context_data())

        sorted_events = sorted(
            all_events,
            key=lambda e: (e["created_at"], e["subheader"].lower()),
            reverse=True,
        )
        return sorted_events
