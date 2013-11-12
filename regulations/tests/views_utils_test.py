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
            self.cfgov_gai = settings.EREGS_GA['CFGOV']['ID']
            self.cfgov_gas = settings.EREGS_GA['CFGOV']['SITE']


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
            settings.EREGS_GA_CFGOV_ID = self.cfgov_gai
        elif hasattr(settings, 'EREGS_GA_CFGOV_ID'):
            del(settings.EREGS_GA_CFGOV_ID)
        if hasattr(self, 'cfgov_gas'):
            settings.EREGS_GA_CFGOV_SITE = self.cfgov_gas
        elif hasattr(settings, 'EREGS_GA_CFGOV_SITE'):
            del(settings.EREGS_GA_CFGOV_SITE)


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

        settings.DEBUG = True
        add_extras(context)
        self.assertEqual('source', context['env'])

        settings.DEBUG = False
        add_extras(context)
        self.assertEqual('built', context['env'])

    def test_add_extras(self):
        context = {}
        add_extras(context)

        self.assertTrue('EREGS_GA_EREGS_ID' in context)
        self.assertTrue('EREGS_GA_EREGS_SITE' in context)
        self.assertTrue('EREGS_GA_CFGOV_ID' in context)
        self.assertTrue('EREGS_GA_CFGOV_SITE' in context)
        self.assertTrue('APP_PREFIX' in context)
        self.assertTrue('env' in context)

    def test_add_extras_gai(self):
        """Make sure we are backwards compatible with GOOGLE_* params"""
        settings.GOOGLE_ANALYTICS_ID = 'googid'
        settings.GOOGLE_ANALYTICS_SITE = 'googsite'
        del(settings.EREGS_GA)

        context = {}
        add_extras(context)
        self.assertEqual('googid', context['EREGS_GA_EREGS_ID'])
        self.assertEqual('googsite', context['EREGS_GA_EREGS_SITE'])

    @patch('regulations.views.utils.table_of_contents')
    def test_first_section(self, table_of_contents):
        table_of_contents.return_value = [
            {'section_id': '204-100'}, {'section_id': '204-101'}]
        first = first_section('204', '2')
        self.assertEqual(first, '204-100')
