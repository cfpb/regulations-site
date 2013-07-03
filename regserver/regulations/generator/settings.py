GOOGLE_ANALYTICS_ID = ''
GOOGLE_ANALYTICS_SITE = ''
API_BASE = ''

OUTPUT_DIR = '/tmp/'
TITLE_PART_NUMBER = ''
REG_VERSION = ''
ACT = ''
ENV = ''

try:
    from local_settings import * 
except ImportError:
    pass
