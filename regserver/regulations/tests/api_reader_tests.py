import os
import shutil
import tempfile
from unittest import TestCase

from mock import patch

from regulations.generator.api_reader import ApiReader


class ClientTest(TestCase):
    @patch('regulations.generator.api_reader.api_client')
    def test_regulation(self, api_client):
        to_return = {'example': 0, 'label': ['204'], 'children': []}
        api_client.ApiClient.return_value.get.return_value = to_return
        reader = ApiReader()
        self.assertEqual(to_return,
                         reader.regulation("label-here", "date-here"))
        self.assertTrue(api_client.ApiClient.return_value.get.called)
        param = api_client.ApiClient.return_value.get.call_args[0][0]
        self.assertTrue('label-here' in param)
        self.assertTrue('date-here' in param)

    @patch('regulations.generator.api_reader.api_client')
    def test_layer(self, api_client):
        to_return = {'example': 1}
        api_client.ApiClient.return_value.get.return_value = to_return
        reader = ApiReader()
        self.assertEqual(
            to_return,
            reader.layer("layer-here", "label-here", "date-here"))
        get = api_client.ApiClient.return_value.get
        self.assertEqual(1, get.call_count)
        param = api_client.ApiClient.return_value.get.call_args[0][0]
        self.assertTrue('layer-here' in param)
        self.assertTrue('label' in param)   # grabs the root
        self.assertTrue('date-here' in param)

        #   Cache
        self.assertEqual(
            to_return,
            reader.layer("layer-here", "label-abc", "date-here"))
        self.assertEqual(1, get.call_count)

        self.assertEqual(
            to_return,
            reader.layer("layer-here", "lablab", "date-here"))
        self.assertEqual(2, get.call_count)
        param = get.call_args[0][0]
        self.assertTrue('layer-here' in param)
        self.assertTrue('lablab' in param)
        self.assertTrue('date-here' in param)

    @patch('regulations.generator.api_reader.api_client')
    def test_notices(self, api_client):
        to_return = {'example': 1}
        api_client.ApiClient.return_value.get.return_value = to_return
        reader = ApiReader()
        self.assertEqual(to_return, reader.notices())
        get = api_client.ApiClient.return_value.get
        self.assertTrue(get.called)
        param = get.call_args[0][0]

        self.assertEqual(to_return, reader.notices(part='p'))
        self.assertTrue(get.called)
        self.assertEqual({'part': 'p'}, get.call_args[0][1])

    @patch('regulations.generator.api_reader.api_client')
    def test_regversion(self, api_client):
        to_return = {}
        api_client.ApiClient.return_value.get.return_value = to_return
        reader = ApiReader()
        self.assertEqual(to_return, reader.regversions('765'))
        get = api_client.ApiClient.return_value.get
        self.assertTrue(get.called)
        param = get.call_args[0][0]
        self.assertTrue('765' in param)

    @patch('regulations.generator.api_reader.api_client')
    def test_notice(self, api_client):
        to_return = {'example': 1}
        api_client.ApiClient.return_value.get.return_value = to_return
        reader = ApiReader()
        self.assertEqual(to_return, reader.notice("doc"))
        get = api_client.ApiClient.return_value.get
        self.assertTrue(get.called)
        param = get.call_args[0][0]
        self.assertTrue('doc' in param)

    @patch('regulations.generator.api_reader.api_client')
    def test_diff(self, api_client):
        to_return = {'example': 1}
        api_client.ApiClient.return_value.get.return_value = to_return
        reader = ApiReader()
        self.assertEqual(to_return, reader.diff("204", "old", "new"))

        get = api_client.ApiClient.return_value.get
        self.assertTrue(get.called)
        param = get.call_args[0][0]
        self.assertTrue('204' in param)
        self.assertTrue('old' in param)
        self.assertTrue('new' in param)

    @patch('regulations.generator.api_reader.api_client')
    def test_reg_cache(self, api_client):
        child = {
            'text': 'child',
            'children': [],
            'label': ['923', 'a']
        }
        to_return = {
            'text': 'parent',
            'label': ['923'],
            'children': [child]
        }
        api_client.ApiClient.return_value.get.return_value = to_return
        reader = ApiReader()

        self.assertEqual(to_return, reader.regulation('923', 'ver'))
        self.assertEqual(to_return, reader.regulation('923', 'ver'))
        self.assertEqual(child, reader.regulation('923-a', 'ver'))
        get = api_client.ApiClient.return_value.get
        self.assertEqual(1, get.call_count)

        get.return_value = to_return
        reader.regulation('923-b', 'ver')
        self.assertEqual(2, get.call_count)
