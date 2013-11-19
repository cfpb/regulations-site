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

NOSE_ARGS = [
    '--exclude-dir=regulations/uitests'
]

try:
    from local_settings import *
except ImportError:
    pass
