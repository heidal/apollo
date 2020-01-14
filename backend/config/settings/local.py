from .base import *

CORS_ORIGIN_ALLOW_ALL = True

THIRD_PARTY_APPS += [
    'debug_toolbar'
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]
