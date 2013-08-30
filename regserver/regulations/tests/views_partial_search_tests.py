import re
from unittest import TestCase

from django.test.client import Client
from mock import patch

from regulations.views.partial_search import *


class PartialSearchTest(TestCase):
    """Integration tests for search"""

    @patch('regulations.views.partial_search.api_reader')
    def test_get(self, api_reader):
        api_reader.ApiReader.return_value.search.return_value = {
            'total_hits': 3333,
            'results': [
                {'label': ['111', '22'], 'text': 'tttt', 'version': 'vvv'},
                {'label': ['111', '24', 'a'], 'text': 'o', 'version': 'vvv'},
                {'label': ['111', '25'], 'text': 'more', 'version': 'vvv'}
            ]
        }
        response = Client().get('/partial/search?version=vvv&q=none')
        self.assertTrue('111-22' in response.content)
        self.assertTrue('111.22' in response.content)
        self.assertTrue('111-24-a' in response.content)
        self.assertTrue('111.24(a)' in response.content)
        self.assertTrue('111-25' in response.content)
        self.assertTrue('111.25' in response.content)
        print response.content[:100]
        self.assertTrue('3333' in response.content)

    def test_get_404(self):
        response = Client().get('/partial/search?version=vvv')
        self.assertEqual(404, response.status_code)
        response = Client().get('/partial/search?q=vvv')
        self.assertEqual(404, response.status_code)
