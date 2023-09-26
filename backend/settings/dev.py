import os

from backend.settings.base import *

ALLOWED_HOSTS = ("localhost", ".localhost", "192.168.1.3")

# CSRF_TRUSTED_ORIGINS = [
#     "http://localhost:3000",
#     "http://app.localhost:3000",
#     "http://app.192.168.1.3:3000",
#     "http://localhost:8000",
# ]

CSRF_TRUSTED_ORIGINS = ["https://*.localhost", "http://app.localhost:3000"]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = [
    # "http://localhost:3000",
    "http://app.localhost:3000",
    "http://app.192.168.1.3:3000",
    # "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    # "http://localhost:3000",
    "http://app.localhost:3000",
    "http://app.192.168.1.3:3000",
]

CSRF_COOKIE_DOMAIN = "localhost"


CSRF_COOKIE_SECURE = True
