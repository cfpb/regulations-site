GOOGLE_ANALYTICS_ID = ''
GOOGLE_ANALYTICS_SITE = ''
API_BASE = ''

REGULATION_VERSION = '2011-31725'
OUTPUT_DIR = '/tmp/'

try:
    from local_settings import * 
except ImportError:
    pass
