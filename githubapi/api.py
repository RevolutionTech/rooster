from github import Github
from social_django.utils import load_strategy

from githubapi.events import EVENT_CLASSES


class GithubAPI:
    def __init__(self, user):
        strategy = load_strategy()
        user_social_auth = user.social_auth.get()
        access_token = user_social_auth.get_access_token(strategy)
        self.api = Github(access_token)
        github_authenticated_user = self.api.get_user()
        self.github_named_user = self.api.get_user(github_authenticated_user.login)

    def event_from_github_event(self, github_event):
        for event_class in EVENT_CLASSES:
            if (
                event_class.api_type == github_event.type
                and event_class.action == github_event.payload["action"]
            ):
                return event_class(self.api, github_event)

    def get_events(self):
        unique_keys = set()
        all_events = []

        for github_event in self.github_named_user.get_events():
            event = self.event_from_github_event(github_event)
            if event:
                unique_key = event.unique_key()
                if unique_key not in unique_keys:
                    unique_keys.add(unique_key)
                    all_events.append(event)

        sorted_events = sorted(
            all_events, key=lambda e: (e.created_at, e.subheader.lower()), reverse=True
        )
        return [e.get_context_data() for e in sorted_events]
