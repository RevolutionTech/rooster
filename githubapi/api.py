import datetime
import functools

import pytz
from django.utils import timezone
from github import Github
from social_django.utils import load_strategy

from githubapi.events import EVENT_CLASSES


class GithubAPI:
    MAX_NUM_DAYS_OF_EVENTS = 5

    def __init__(self, user):
        strategy = load_strategy()
        user_social_auth = user.social_auth.get()
        access_token = user_social_auth.get_access_token(strategy)
        self.api = Github(access_token)
        github_authenticated_user = self.api.get_user()
        self.github_named_user = self.get_user(github_authenticated_user.login)

    @functools.lru_cache
    def get_user(self, login):
        return self.api.get_user(login)

    @functools.lru_cache
    def get_repo(self, repo_id):
        return self.api.get_repo(repo_id)

    def get_github_events(self):
        """
        Limit the events fetched from GitHub to span over a fixed number of days.
        """
        most_recent_event_date = None
        for github_event in self.github_named_user.get_events():
            event_created_at_utc = pytz.utc.localize(github_event.created_at)
            event_created_at_date = timezone.localtime(event_created_at_utc).date()
            if most_recent_event_date is None:
                most_recent_event_date = event_created_at_date

            if event_created_at_date <= most_recent_event_date - datetime.timedelta(
                days=self.MAX_NUM_DAYS_OF_EVENTS
            ):
                break
            else:
                yield github_event

    def event_from_github_event(self, github_event):
        for event_class in EVENT_CLASSES:
            if (
                event_class.api_type == github_event.type
                and event_class.action == github_event.payload["action"]
            ):
                return event_class(self, github_event)

    def get_unique_events(self):
        unique_keys = set()
        for github_event in self.get_github_events():
            event = self.event_from_github_event(github_event)
            if event:
                unique_key = event.unique_key()
                if unique_key not in unique_keys:
                    unique_keys.add(unique_key)
                    yield event

    def get_events(self):
        return [e.to_json() for e in self.get_unique_events()]

    def get_events_for_dashboard(self):
        all_events = self.get_unique_events()
        sorted_events = sorted(
            all_events,
            key=lambda e: (
                e.created_at.date(),
                e.subheader.lower(),
                e.created_at.time(),
            ),
            reverse=True,
        )
        return [e.get_context_data() for e in sorted_events]
