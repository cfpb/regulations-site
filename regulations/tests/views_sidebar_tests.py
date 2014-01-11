import re
from unittest import TestCase

from mock import patch
from django.test.client import Client

from regulations.generator import node_types


class ViewsSideBarViewTest(TestCase):
    """Integration tests for the sidebar"""

    @patch('regulations.views.sidebar.api_reader')
    def test_get(self, api_reader):
        api_reader.ApiReader.return_value.layer.return_value = {
            '1111-7': [
                {'reference': ['1992-1', '1111-7']},
                {'reference': ['1992-2', '1111-7']},
            ],
            '1111-7-a': [{'reference': ['1992-1', '1111-7-a']}]
        }
        api_reader.ApiReader.return_value.regulation.return_value = {
            'label': ['876', '12'],
            'node_type': node_types.REGTEXT,
            'children': [
                {'label': ['876', '12', 'a'], 'children': [],
                 'node_type': node_types.REGTEXT},
                {'label': ['876', '12', 'b'], 'children': [],
                 'node_type': node_types.REGTEXT},
                {'label': ['876', '12', 'c'], 'node_type': node_types.REGTEXT,
                 'children': [
                     {'label': ['876', '12', 'c', '1'], 'children': [],
                      'node_type': node_types.REGTEXT}]}
            ]
        }
        response = Client().get('/partial/sidebar/1111-7/verver')
        self.assertTrue(bool(re.search(r'\b7\b', response.content)))
        self.assertTrue('7(a)' in response.content)
        self.assertTrue('1992-2' in response.content)
        self.assertTrue('1111-7' in response.content)
        self.assertTrue('1992-1' in response.content)
        self.assertTrue('1111-7-a' in response.content)
        self.assertTrue('876-12' in response.content)
        self.assertTrue('876-12-a' in response.content)
        self.assertTrue('876-12-b' in response.content)
        self.assertTrue('876-12-c' in response.content)
        self.assertTrue('876-12-c-1' in response.content)
        self.assertTrue('12(a)' in response.content)
        self.assertTrue('12(b)' in response.content)
        self.assertTrue('12(c)' in response.content)
        self.assertTrue('12(c)(1)' in response.content)

    @patch('regulations.views.sidebar.api_reader')
    def test_get_interp(self, api_reader):
        api_reader.ApiReader.return_value.layer.return_value = {}
        api_reader.ApiReader.return_value.regulation.return_value = {
            'label': ['876', 'Interp'],
            'node_type': node_types.INTERP,
            'children': [
                {'label': ['876', '12', 'a', 'Interp'], 'children': [],
                 'node_type': node_types.INTERP},
                {'label': ['876', '12', 'Interp', '1'], 'children': [],
                 'node_type': node_types.INTERP}
            ]
        }
        response = Client().get('/partial/sidebar/876-Interp/verver')
        self.assertTrue('Comment for 876.12(a)' in response.content)
        self.assertTrue('Comment for 876.12-1' in response.content)
        self.assertTrue('876-Interp/verver#876-12-a-Interp'
                        in response.content)
        self.assertTrue('876-Interp/verver#876-12-Interp-1'
                        in response.content)
