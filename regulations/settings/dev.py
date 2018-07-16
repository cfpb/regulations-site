from .base import *

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# Add static file directories that live in subdirectories under static.in.
STATIC_IN = root('static.in')
STATICFILES_DIRS += tuple(
    os.path.join(STATIC_IN, d)
    for d in os.listdir(STATIC_IN)
    if os.path.isdir(os.path.join(STATIC_IN, d))
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
