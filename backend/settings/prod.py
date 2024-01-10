import os

from backend.settings.base import *


ALLOWED_HOSTS = ["api-us-east-1.traceit.io"]


CSRF_TRUSTED_ORIGINS = [
    "https://*.traceit.io",
    "https://traceit.io",
    "https://api-us-east-1.traceit.io",
]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = ["https://app.traceit.io", "https://traceit.io"]
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = ["https://app.traceit.io", "https://traceit.io"]

CSRF_COOKIE_DOMAIN = "traceit.io"


CSRF_COOKIE_SECURE = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
SERVER_EMAIL = os.environ.get("FROM_EMAIL_ADDRESS", "info@traceit.io")
DEFAULT_FROM_EMAIL = os.environ.get("FROM_EMAIL_ADDRESS", "info@traceit.io")

EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 587)
EMAIL_USE_TLS = False if os.environ.get("EMAIL_DISABLE_TLS") == "True" else True
