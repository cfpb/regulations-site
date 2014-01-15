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
            '876-12': [
                {'reference': ['1992-1', '876-12']},
                {'reference': ['1992-2', '876-12']},
            ],
            '876-12-a': [{'reference': ['1992-1', '876-12-a']}]
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

        sxs_start = response.content.find('<section id="sxs-list"')
        sxs_end = response.content.find('</section>', sxs_start)
        sxs = response.content[sxs_start:sxs_end]

        permalinks_start = response.content.find('<section id="permalinks"')
        permalinks_end = response.content.find('</section>', permalinks_start)
        permalinks = response.content[permalinks_start:permalinks_end]

        self.assertTrue(bool(re.search(r'\b12\b', sxs)))
        self.assertTrue('12(a)' in sxs)
        self.assertTrue('1992-2' in sxs)
        self.assertTrue('876-12' in sxs)
        self.assertTrue('1992-1' in sxs)
        self.assertTrue('876-12-a' in sxs)
        self.assertFalse('876-12-b' in sxs)

        self.assertTrue(bool(re.search(r'\b12\b', permalinks)))
        self.assertTrue('876-12' in permalinks)
        self.assertTrue('876-12-a' in permalinks)
        self.assertTrue('876-12-b' in permalinks)
        self.assertTrue('876-12-c' in permalinks)
        self.assertTrue('876-12-c-1' in permalinks)
        self.assertTrue('12(a)' in permalinks)
        self.assertTrue('12(b)' in permalinks)
        self.assertTrue('12(c)' in permalinks)
        self.assertTrue('12(c)(1)' in permalinks)
        self.assertFalse('1992-1' in permalinks)

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
