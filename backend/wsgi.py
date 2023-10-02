"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from decouple import config
from dotenv import load_dotenv
from pathlib import Path

from django.core.wsgi import get_wsgi_application


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env"))

DEBUG = config("DEBUG", default=False, cast=bool)

if DEBUG:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.dev")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.prod")

application = get_wsgi_application()
