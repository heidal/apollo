import socket

from .base import *

CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + "1"]
ALLOWED_HOSTS += ["apollo.localhost"]
