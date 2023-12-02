from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# create a Celery instance and configure it using the settings from Django
celery_app = Celery("backend")

# Load task modules from all registered Django app configs.
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in all installed apps
celery_app.autodiscover_tasks()
