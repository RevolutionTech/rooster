from django.contrib.auth.models import User
from django.db import models
from django_cryptography.fields import encrypt


class UserSettings(models.Model):

    JIRA_API_KEY_LENGTH = 24

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    jira_server_url = models.URLField(blank=True, verbose_name="JIRA Server URL")
    jira_email = models.EmailField(blank=True, verbose_name="JIRA Email")
    jira_api_key = encrypt(
        models.CharField(
            max_length=JIRA_API_KEY_LENGTH, blank=True, verbose_name="JIRA API Key"
        )
    )

    def __str__(self):
        return str(self.user)
