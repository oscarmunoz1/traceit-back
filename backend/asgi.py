"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from decouple import config
from dotenv import load_dotenv

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env"))

DEBUG = config("DEBUG", default=False, cast=bool)

if DEBUG:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.dev")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.prod")

application = get_asgi_application()
