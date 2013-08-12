from .base import *

DEBUG = False

ALLOWED_HOSTS=['locahost', '127.0.0.1']

STATIC_ROOT = ''

OFFLINE_OUTPUT_DIR = '/tmp/'

STATICFILES_DIRS = (
    root('static'),
)

TEMPLATE_DIRS += (root('regulations/generator/templates'), )

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = 'eregs'

try:
    from local_settings import *
except ImportError:
    pass
