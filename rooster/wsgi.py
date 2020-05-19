"""
WSGI config for rooster project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rooster.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "BaseConfig")


from configurations.wsgi import get_wsgi_application  # isort:skip


application = get_wsgi_application()
