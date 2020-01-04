class BaseEventType:
    pass


class PullRequestEventType(BaseEventType):
    api_type = "PullRequestEvent"
    action = "opened"
    subheader = "Pull Requests"


class PullRequestCommentEventType(BaseEventType):
    api_type = "PullRequestReviewCommentEvent"
    action = "created"
    subheader = "PR Reviews"


EVENT_TYPES = [PullRequestEventType, PullRequestCommentEventType]


def event_type_from_github_event(github_event):
    for event_type in EVENT_TYPES:
        if (
            event_type.api_type == github_event.type
            and event_type.action == github_event.payload["action"]
        ):
            return event_type
