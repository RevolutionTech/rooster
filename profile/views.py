from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from githubapi.api import GithubAPI


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        api = GithubAPI(self.request.user)
        context["events"] = api.get_events()

        return context
