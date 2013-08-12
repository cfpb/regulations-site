from .base import *

DEBUG = False

TEMPLATE_DIRS += (root('regulations/generator/templates'), )

OFFLINE_OUTPUT_DIR = '/tmp/'

STATICFILES_DIRS = (
    root('static'),
)


try:
    from local_settings import *
except ImportError:
    pass
