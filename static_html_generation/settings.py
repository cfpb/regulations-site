GOOGLE_ANALYTICS_ID = ''
GOOGLE_ANALYTICS_SITE = ''
API_BASE = ''

OUTPUT_DIR = '/tmp/'

try:
    from local_settings import * 
except ImportError:
    pass
