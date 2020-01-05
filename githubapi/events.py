class BaseEvent:
    def __init__(self, api, github_event):
        self.api = api
        self.created_at = github_event.created_at
        self.repo = github_event.repo
        self.pull_request = github_event.payload["pull_request"]

        # TODO: Memoize api.get_user()
        self.pull_request_author = self.api.get_user(self.pull_request["user"]["login"])

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
            "pull_request": {
                "title": self.pull_request["title"],
                "url": self.pull_request["html_url"],
                "author": self.pull_request_author.name
                or self.pull_request_author.login,
            },
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
