import factory

from profile.models import UserSettings
from rooster.factories import UserFactory


class UserSettingsFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserSettings

    user = factory.SubFactory(UserFactory)
    jira_server_url = factory.Faker("url")
    jira_email = factory.Faker("email")
    jira_api_key = factory.Faker("password")
