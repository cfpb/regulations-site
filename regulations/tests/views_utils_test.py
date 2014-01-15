#vim: set encoding=utf-8
from unittest import TestCase
from mock import patch

from django.conf import settings

from regulations.views.utils import *


class UtilsTest(TestCase):
    def setUp(self):
        if hasattr(settings, 'GOOGLE_ANALYTICS_ID'):
            self.old_gai = settings.GOOGLE_ANALYTICS_ID
        if hasattr(settings, 'GOOGLE_ANALYTICS_SITE'):
            self.old_gas = settings.GOOGLE_ANALYTICS_SITE
        if hasattr(settings, 'EREGS_GA'):
            self.eregs_gai = settings.EREGS_GA['EREGS']['ID']
            self.eregs_gas = settings.EREGS_GA['EREGS']['SITE']
            self.cfgov_gai = settings.EREGS_GA['ALT']['ID']
            self.cfgov_gas = settings.EREGS_GA['ALT']['SITE']
        if hasattr(settings, 'JS_DEBUG'):
            self.old_js_debug = settings.JS_DEBUG

    def tearDown(self):
        if hasattr(self, 'old_gai'):
            settings.GOOGLE_ANALYTICS_ID = self.old_gai
        elif hasattr(settings, 'GOOGLE_ANALYTICS_ID'):
            del(settings.GOOGLE_ANALYTICS_ID)
        if hasattr(self, 'old_gas'):
            settings.GOOGLE_ANALYTICS_SITE = self.old_gas
        elif hasattr(settings, 'GOOGLE_ANALYTICS_SITE'):
            del(settings.GOOGLE_ANALYTICS_SITE)

        if hasattr(self, 'eregs_gai'):
            settings.EREGS_GA_EREGS_ID = self.eregs_gai
        elif hasattr(settings, 'EREGS_GA_EREGS_ID'):
            del(settings.EREGS_GA_EREGS_ID)
        if hasattr(self, 'eregs_gas'):
            settings.EREGS_GA_EREGS_SITE = self.eregs_gas
        elif hasattr(settings, 'EREGS_GA_EREGS_SITE'):
            del(settings.EREGS_GA_EREGS_SITE)

        if hasattr(self, 'cfgov_gai'):
            settings.EREGS_GA_ALT_ID = self.cfgov_gai
        elif hasattr(settings, 'EREGS_GA_ALT_ID'):
            del(settings.EREGS_GA_ALT_ID)
        if hasattr(self, 'cfgov_gas'):
            settings.EREGS_GA_ALT_SITE = self.cfgov_gas
        elif hasattr(settings, 'EREGS_GA_ALT_SITE'):
            del(settings.EREGS_GA_ALT_SITE)

        if hasattr(self, 'old_js_debug'):
            settings.JS_DEBUG = self.old_js_debug

    def test_get_layer_list(self):
        names = 'meta,meta,GRAPHICS,fakelayer,internal'
        layer_list = get_layer_list(names)
        self.assertEquals(set(['meta', 'internal', 'graphics']), layer_list)

    @patch('regulations.generator.generator.LayerCreator.get_layer_json')
    def test_handle_specified_layers(self, get_layer_json):
        get_layer_json.return_value = {'layer': 'layer'}

        layer_names = 'graphics,meta'
        appliers = handle_specified_layers(layer_names, '205', '2013-1')
        self.assertEquals(3, len(appliers))

    def test_add_extras_env(self):
        context = {}

        settings.JS_DEBUG = True
        add_extras(context)
        self.assertEqual('source', context['env'])

        settings.JS_DEBUG = False
        add_extras(context)
        self.assertEqual('built', context['env'])

        del(settings.JS_DEBUG)
        add_extras(context)
        self.assertEqual('built', context['env'])

    def test_add_extras(self):
        context = {}
        settings.EREGS_GA = {
            'EREGS': {'ID': 'eregs-ga-id', 'SITE': 'eregs'},
            'ALT': {'ID': 'alt-ga-id', 'SITE': 'alt'}
        }
        add_extras(context)

        self.assertTrue('APP_PREFIX' in context)
        self.assertTrue('env' in context)

        self.assertEquals('eregs-ga-id', context['EREGS_GA_EREGS_ID'])
        self.assertEquals('eregs', context['EREGS_GA_EREGS_SITE'])
        self.assertEquals('alt-ga-id', context['EREGS_GA_ALT_ID'])
        self.assertEquals('alt', context['EREGS_GA_ALT_SITE'])

    def test_add_extras_gai(self):
        """Make sure we are backwards compatible with GOOGLE_* params"""
        settings.GOOGLE_ANALYTICS_ID = 'googid'
        settings.GOOGLE_ANALYTICS_SITE = 'googsite'
        del(settings.EREGS_GA)

        context = {}
        add_extras(context)
        self.assertEqual('googid', context['EREGS_GA_EREGS_ID'])
        self.assertEqual('googsite', context['EREGS_GA_EREGS_SITE'])

    @patch('regulations.views.utils.fetch_toc')
    def test_first_section(self, fetch_toc):
        fetch_toc.return_value = [
            {'section_id': '204-100', 'index': ['204', '100']},
            {'section_id': '204-101', 'index': ['204', '101']}]
        first = first_section('204', '2')
        self.assertEqual(first, '204-100')
