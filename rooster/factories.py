import factory
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth


class UserFactory(factory.DjangoModelFactory):

    _PASSWORD = "abc123"

    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.LazyAttribute(lambda user: f"{user.username}@gmail.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    social_auth = factory.RelatedFactory(
        "rooster.factories.UserSocialAuthFactory", "user"
    )
    settings = factory.RelatedFactory(
        "profile.tests.factories.UserSettingsFactory", "user"
    )


class UserSocialAuthFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserSocialAuth

    user = factory.SubFactory(UserFactory)
    uid = factory.Sequence(lambda n: n)
    extra_data = factory.LazyAttribute(
        lambda user_social_auth: {
            "auth_time": 1_546_300_800,
            "id": user_social_auth.uid,
            "expires": None,
            "login": user_social_auth.user.username,
            "access_token": "abc123",
            "token_type": "bearer",
        }
    )
