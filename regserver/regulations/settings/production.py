from .base import *

DEBUG = False
ALLOWED_HOSTS=['locahost', '127.0.0.1']

#In production, this needs to be set to the directory where the static files
#should end up:
#STATIC_ROOT = ''

OFFLINE_OUTPUT_DIR = '/tmp/'

#In production, set this to what makes sense for you. 
CACHE_MIDDLEWARE_SECONDS = 600

try:
    from local_settings import *
except ImportError:
    pass
