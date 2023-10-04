import os

from backend.settings.base import *


ALLOWED_HOSTS = ["api-us-east-1.traceit.io"]


CSRF_TRUSTED_ORIGINS = [".traceit.io", "traceit.io", "api-us-east-1.traceit.io"]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = ["https://app.traceit.io", "https://traceit.io"]
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = ["https://app.traceit.io", "https://traceit.io"]

CSRF_COOKIE_DOMAIN = "traceit.io"


CSRF_COOKIE_SECURE = True
