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
                {'label': ['111', '22'], 'text': 'tttt', 'version': 'vvv', 'title':"consumer's"},
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
             'timeline': 'timeytimey'}
        ]
        response = Client().get('/partial/search/111?version=vvv&q=none')
        self.assertTrue('111-22' in response.content)
        self.assertTrue('111.22' in response.content)
        self.assertTrue('111-24-a' in response.content)
        self.assertTrue('111.24(a)' in response.content)
        self.assertTrue('111-25' in response.content)
        self.assertTrue('111.25' in response.content)
        self.assertTrue('3333' in response.content)
        self.assertTrue('Consumer&#39;s' in response.content)

    @patch('regulations.views.partial_search.api_reader')
    @patch('regulations.views.partial_search.fetch_grouped_history')
    def test_root_info(self, fetch_grouped_history, api_reader):
        api_reader.ApiReader.return_value.search.return_value = {
            'total_hits': 3,
            'results': [
                {'label': ['444', '22'], 'text': 'tttt', 'version': 'vvv', 'title':"consumer's"},
                {'label': ['444', '24', 'a'], 'text': 'o', 'version': 'vvv'},
                {'label': ['444'], 'text': 'more', 'version': 'vvv'}
            ]
        }
        fetch_grouped_history.return_value = [
            {'notices': [{'document_number': 'bbb',
                          'effective_on': date(2012, 12, 12)}]},
            {'notices': [{'document_number': 'ccc',
                          'effective_on': date(2001, 1, 1)},
                         {'document_number': 'vvv',
                          'effective_on': date(2003, 4, 5)}],
             'timeline': 'timeytimey'}
        ]
        response = Client().get('/partial/search/444?version=vvv&q=none')
        self.assertTrue('2 results' in response.content)

    @patch('regulations.views.partial_search.api_reader')
    @patch('regulations.views.partial_search.fetch_grouped_history')
    @patch('regulations.generator.section_url.fetch_toc')
    def test_subinterp(self, fetch_toc, fetch_grouped_history, api_reader):
        fetch_toc.return_value = [
            {'index': ['444', 'Subpart', 'B'], 'is_subpart': True,
             'section_id': '444-Subpart-B', 'sub_toc': [
                {'index': ['444', '22'], 'section_id': '444-22',
                 'is_section': True}]},
            {'index': ['444', 'Interp'], 'section_id': '444-Interp',
             'sub_toc': [
                {'index': ['444', 'Interp', 'h1'],
                 'section_id': '444-Interp-h1'},
                {'index': ['444', 'Subpart', 'B', 'Interp'],
                 'section_id': '444-Subpart-B-Interp'}]}
        ]
        api_reader.ApiReader.return_value.search.return_value = {
            'total_hits': 3,
            'results': [
                {'label': ['444', '22', 'Interp'], 'text': 'tttt',
                 'version': 'vvv', 'title':"consumer's"},
                {'label': ['444', 'Interp', 'h1', 'p5'], 'text': 'o',
                 'version': 'vvv'}
            ]
        }
        fetch_grouped_history.return_value = [
            {'notices': [{'document_number': 'bbb',
                          'effective_on': date(2012, 12, 12)}]},
            {'notices': [{'document_number': 'ccc',
                          'effective_on': date(2001, 1, 1)},
                         {'document_number': 'vvv',
                          'effective_on': date(2003, 4, 5)}],
             'timeline': 'timeytimey'}
        ]

        response = Client().get('/partial/search/444?version=vvv&q=other')
        self.assertTrue('444-Subpart-B-Interp' in response.content)
        self.assertTrue('444-Interp-h1' in response.content)

    @patch('regulations.views.partial_search.api_reader')
    @patch('regulations.views.partial_search.fetch_grouped_history')
    def test_no_results(self, fetch_grouped_history, api_reader):
        api_reader.ApiReader.return_value.search.return_value = {
            'total_hits': 0,
            'results': []
        }
        fetch_grouped_history.return_value = [
            {'notices': [{'document_number': 'bbb',
                          'effective_on': date(2012, 12, 12)}]},
            {'notices': [{'document_number': 'ccc',
                          'effective_on': date(2001, 1, 1)},
                         {'document_number': 'vvv',
                          'effective_on': date(2003, 4, 5)}],
             'timeline': 'timeytimey'}
        ]
        response = Client().get('/partial/search/121?version=vvv&q=none')
        self.assertTrue('4/5/2003' in response.content)

    def test_get_400(self):
        response = Client().get('/partial/search/111?version=vvv')
        self.assertEqual(400, response.status_code)
        response = Client().get('/partial/search/111?q=vvv')
        self.assertEqual(400, response.status_code)

    def test_add_prev_next(self):
        view = PartialSearch()
        context = {'results': {'total_hits': 77}}
        view.add_prev_next(0, context)
        self.assertFalse('previous' in context)
        self.assertEqual(context['next'], {'page': 1, 'length': 10})

        del context['next']
        view.add_prev_next(5, context)
        self.assertEqual(context['previous'], {'page': 4, 'length': 10})
        self.assertEqual(context['next'], {'page': 6, 'length': 10})

        del context['previous']
        del context['next']
        view.add_prev_next(6, context)
        self.assertEqual(context['previous'], {'page': 5, 'length': 10})
        self.assertEqual(context['next'], {'page': 7, 'length': 7})

        del context['previous']
        del context['next']
        view.add_prev_next(7, context)
        self.assertEqual(context['previous'], {'page': 6, 'length': 10})
        self.assertFalse('next' in context)
