from profile.models import UserSettings

from jira import JIRA, JIRAError


class JiraAPI:
    JQL_IN_PROGRESS = (
        'assignee = currentUser() AND status = "In Progress" ORDER BY updated DESC'
    )

    def __init__(self, user):
        self.valid_credentials = False

        try:
            settings = UserSettings.objects.get(user=user)
        except UserSettings.DoesNotExist:
            return

        if settings.jira_server_url:
            try:
                self.api = JIRA(
                    {"server": settings.jira_server_url},
                    basic_auth=(settings.jira_email, settings.jira_api_key),
                )
                self.valid_credentials = True
            except JIRAError:
                pass

    def get_in_progress_tickets(self):
        if self.valid_credentials:
            issues_in_progress = self.api.search_issues(self.JQL_IN_PROGRESS)
            return [
                {
                    "issue_key": issue.key,
                    "summary": issue.fields.summary,
                    "url": issue.permalink(),
                }
                for issue in issues_in_progress
            ]
