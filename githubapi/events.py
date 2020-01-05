class BaseEvent:
    def __init__(self, github_event):
        self.github_event = github_event

    def get_context_data(self):
        repo = self.github_event.repo
        payload = self.github_event.payload
        pull_request = payload["pull_request"]
        pr_title = pull_request["title"]

        return {
            "created_at": self.github_event.created_at,
            "subheader": self.subheader,
            "repo": {"name": repo.name, "url": repo.html_url},
            "pull_request": {"title": pr_title},
        }


class PullRequestEvent(BaseEvent):
    api_type = "PullRequestEvent"
    action = "opened"
    subheader = "Pull Requests"


class PullRequestCommentEvent(BaseEvent):
    api_type = "PullRequestReviewCommentEvent"
    action = "created"
    subheader = "PR Reviews"


EVENT_CLASSES = [PullRequestEvent, PullRequestCommentEvent]


def event_from_github_event(github_event):
    for event_class in EVENT_CLASSES:
        if (
            event_class.api_type == github_event.type
            and event_class.action == github_event.payload["action"]
        ):
            return event_class(github_event)
