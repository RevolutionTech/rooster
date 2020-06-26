"""
Django settings for rooster project.

"""

import os

from configurations import Configuration, values


class BaseConfig(Configuration):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = values.SecretValue()
    DEBUG = True
    ALLOWED_HOSTS = []

    # Application definition
    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django_s3_sqlite",
        "django_s3_storage",
        "social_django",
        "rest_framework",
        "tz_detect",
        "githubapi.apps.GithubApiConfig",
        "jiraapi.apps.JiraApiConfig",
        "profile.apps.ProfileConfig",
    ]
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "tz_detect.middleware.TimezoneMiddleware",
    ]
    ROOT_URLCONF = "rooster.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [os.path.join(BASE_DIR, "templates")],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ]
            },
        }
    ]
    WSGI_APPLICATION = "rooster.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/3.0/ref/settings/#databases
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

    # Authentication
    AUTHENTICATION_BACKENDS = ["social_core.backends.github.GithubOAuth2"]
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]
    SOCIAL_AUTH_GITHUB_KEY = values.SecretValue()
    SOCIAL_AUTH_GITHUB_SECRET = values.SecretValue()
    SOCIAL_AUTH_GITHUB_SCOPE = ["repo"]
    LOGIN_URL = "/login/github/"
    LOGIN_REDIRECT_URL = "/"
    LOGOUT_REDIRECT_URL = "/"

    # Internationalization
    # https://docs.djangoproject.com/en/3.0/topics/i18n/
    LANGUAGE_CODE = "en-us"
    TIME_ZONE = "UTC"
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.0/howto/static-files/
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]


class ProdConfig(BaseConfig):

    DEBUG = False
    ALLOWED_HOSTS = ["standup.revolutiontech.ca"]
    USE_X_FORWARDED_HOST = True

    # Database
    DATABASES = {
        "default": {
            "ENGINE": "django_s3_sqlite",
            "NAME": "db.sqlite3",
            "BUCKET": "rooster-sqlite3",
        }
    }

    # Static files
    STATICFILES_STORAGE = "django_s3_storage.storage.ManifestStaticS3Storage"
    AWS_S3_BUCKET_NAME_STATIC = "rooster-standup"
    AWS_S3_KEY_PREFIX_STATIC = "static"
    AWS_S3_BUCKET_AUTH = False
    AWS_S3_MAX_AGE_SECONDS = 60 * 60 * 24 * 365  # 1 year
    STATIC_URL = f"https://{AWS_S3_BUCKET_NAME_STATIC}.s3.amazonaws.com/{AWS_S3_KEY_PREFIX_STATIC}/"
    AWS_ACCESS_KEY_ID = values.SecretValue()
    AWS_SECRET_ACCESS_KEY = values.SecretValue()
