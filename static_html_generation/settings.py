GOOGLE_ANALYTICS_ID = ''
GOOGLE_ANALYTICS_SITE = ''
API_BASE = ''

OUTPUT_DIR = '/tmp/'
TITLE_PART_NUMBER = '1005'
REG_VERSION = 'remittances'
EFT_ACT = ['15', '1693'] #Title 15, Section 1693 of the United States Code


try:
    from local_settings import * 
except ImportError:
    pass
