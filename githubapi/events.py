class BaseEvent:
    def __init__(self, github_event):
        self.created_at = github_event.created_at
        self.repo = github_event.repo
        self.pull_request = github_event.payload["pull_request"]

    def unique_key(self):
        """
        Identifier used for uniqueness among other events.

        ie. PullRequestReview events should be unique by date,
            even if multiple comments are made on the same PR in the same day
            so these events are considered to have the same identity.
        """
        return (
            self.__class__,
            self.created_at.date(),
            self.repo.id,
            self.pull_request["id"],
        )

    def get_context_data(self):
        return {
            "created_at": self.created_at,
            "subheader": self.subheader,
            "repo": {"name": self.repo.name, "url": self.repo.html_url},
            "pull_request": {"title": self.pull_request["title"]},
        }


class PullRequestEvent(BaseEvent):
    api_type = "PullRequestEvent"
    action = "opened"
    subheader = "Pull Requests"


class PullRequestReviewEvent(BaseEvent):
    api_type = "PullRequestReviewCommentEvent"
    action = "created"
    subheader = "PR Reviews"


EVENT_CLASSES = [PullRequestEvent, PullRequestReviewEvent]


def event_from_github_event(github_event):
    for event_class in EVENT_CLASSES:
        if (
            event_class.api_type == github_event.type
            and event_class.action == github_event.payload["action"]
        ):
            return event_class(github_event)
