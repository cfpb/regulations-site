from unittest import TestCase
from mock import patch

from django.conf import settings

from regulations.views.utils import *


class UtilsTest(TestCase):
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

        self.assertTrue('GOOGLE_ANALYTICS_ID' in context)
        self.assertTrue('GOOGLE_ANALYTICS_SITE' in context)
        self.assertTrue('APP_PREFIX' in context)
        self.assertTrue('env' in context)

    @patch('regulations.views.utils.table_of_contents')
    def test_first_section(self, table_of_contents):
        table_of_contents.return_value = [
            {'section_id': '204-100'}, {'section_id': '204-101'}]
        first = first_section('204', '2')
        self.assertEqual(first, '204-100')
