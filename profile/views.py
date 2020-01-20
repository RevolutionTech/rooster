from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from githubapi.api import GithubAPI
from jiraapi.api import JiraAPI
from profile.models import UserSettings


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        jira_api = JiraAPI(user)
        github_api = GithubAPI(user)
        context.update(
            {
                "jira_valid_credentials": jira_api.valid_credentials,
                "tickets": jira_api.get_in_progress_tickets(),
                "events": github_api.get_events(),
            }
        )

        return context


class SettingsView(LoginRequiredMixin, UpdateView):
    template_name = "settings.html"
    model = UserSettings
    fields = ["jira_server_url", "jira_email", "jira_api_key"]
    success_url = reverse_lazy("dashboard")

    def get_object(self):
        user_settings, _ = UserSettings.objects.get_or_create(user=self.request.user)
        return user_settings
