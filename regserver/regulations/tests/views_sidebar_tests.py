import re
from unittest import TestCase

from mock import patch

from django.test.client import Client

class ViewsSideBarViewTest(TestCase):
    """Integration tests for the sidebar"""

    @patch('regulations.views.sidebar.api_reader')
    def test_get(self, api_reader):
        api_reader.Client.return_value.layer.return_value = {
            '1111-1': [
                {'reference': ['doc1', '1111-1']},
                {'reference': ['doc2', '1111-1']},
            ],
            '1111-1-a': [{'reference': ['doc1', '1111-1-a']}]
        }
        response = Client().get('/partial/sidebar/1111-1/verver')
        self.assertTrue(bool(re.search(r'\b1111\.1\b', response.content)))
        self.assertTrue('1111.1(a)' in response.content)
