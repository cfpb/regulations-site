from datetime import date
import re
from unittest import TestCase

from django.test.client import Client
from mock import patch

from regulations.views.partial_search import *


class PartialSearchTest(TestCase):
    """Integration tests for search"""

    @patch('regulations.views.partial_search.api_reader')
    @patch('regulations.views.partial_search.fetch_grouped_history')
    def test_get(self, fetch_grouped_history, api_reader):
        api_reader.ApiReader.return_value.search.return_value = {
            'total_hits': 3333,
            'results': [
                {'label': ['111', '22'], 'text': 'tttt', 'version': 'vvv'},
                {'label': ['111', '24', 'a'], 'text': 'o', 'version': 'vvv'},
                {'label': ['111', '25'], 'text': 'more', 'version': 'vvv'}
            ]
        }
        fetch_grouped_history.return_value = [
            {'notices': [{'document_number': 'bbb',
                          'effective_on': date(2012, 12, 12)}]},
            {'notices': [{'document_number': 'ccc',
                          'effective_on': date(2001, 1, 1)},
                         {'document_number': 'vvv',
                          'effective_on': date(2003, 4, 5)}],
             'timeline': 'timeytimey'
            }
        ]
        response = Client().get('/partial/search/111?version=vvv&q=none')
        self.assertTrue('111-22' in response.content)
        self.assertTrue('111.22' in response.content)
        self.assertTrue('111-24-a' in response.content)
        self.assertTrue('111.24(a)' in response.content)
        self.assertTrue('111-25' in response.content)
        self.assertTrue('111.25' in response.content)
        self.assertTrue('3333' in response.content)

        # Version info
        self.assertTrue('timeytimey' in response.content.lower())
        self.assertTrue('4/5/2003' in response.content)

    def test_get_400(self):
        response = Client().get('/partial/search/111?version=vvv')
        self.assertEqual(400, response.status_code)
        response = Client().get('/partial/search/111?q=vvv')
        self.assertEqual(400, response.status_code)
