from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

STATICFILES_DIRS = (
    root('static'),
)

TEMPLATE_DIRS += (root('regulations/generator/templates'), )

CACHES = {
    'default' : {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
    }
}

OFFLINE_OUTPUT_DIR = '/tmp/'

INSTALLED_APPS += (
    'django_nose',
)

MIDDLEWARE_CLASSES += (
    'django.middleware.cache.UpdateCacheMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = 'eregs'

try:
    from local_settings import *
except ImportError:
    pass
