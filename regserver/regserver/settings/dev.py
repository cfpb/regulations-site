from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

STATICFILES_DIRS = (
    root('static'),
)

TEMPLATE_DIRS += (root('regulations/generator/templates'), )

OFFLINE_OUTPUT_DIR = '/tmp/'

INSTALLED_APPS += (
    'django_nose',
)

try:
    from local_settings import *
except ImportError:
    pass
