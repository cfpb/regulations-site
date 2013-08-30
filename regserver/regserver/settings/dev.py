from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

STATICFILES_DIRS = (
    root('static'),
)


OFFLINE_OUTPUT_DIR = '/tmp/'

INSTALLED_APPS += (
    'django_nose',
)

CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': '/tmp/django_cache',
}


try:
    from local_settings import *
except ImportError:
    pass
