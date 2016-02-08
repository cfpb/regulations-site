from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

STATICFILES_DIRS = (
    root('static'),
)


CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
CACHES['eregs_longterm_cache']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
CACHES['api_cache']['TIMEOUT'] = 5  # roughly per request

OFFLINE_OUTPUT_DIR = '/tmp/'

INSTALLED_APPS += (
    'django_nose',
)

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=regulations',
    '--exclude-dir=regulations/uitests'
]

try:
    from local_settings import *
except ImportError:
    pass
