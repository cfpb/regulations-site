import re
from unittest import TestCase

from mock import patch

from django.test.client import Client


class ViewsSideBarViewTest(TestCase):
    """Integration tests for the sidebar"""

    @patch('regulations.views.sidebar.api_reader')
    def test_get(self, api_reader):
        api_reader.ApiReader.return_value.layer.return_value = {
            '1111-1': [
                {'reference': ['1992-1', '1111-1']},
                {'reference': ['1992-2', '1111-1']},
            ],
            '1111-1-a': [{'reference': ['1992-1', '1111-1-a']}]
        }
        response = Client().get('/partial/sidebar/1111-1/verver')
        self.assertTrue(bool(re.search(r'\b1111\.1\b', response.content)))
        self.assertTrue('1111.1(a)' in response.content)
        self.assertTrue('1992-2' in response.content)
        self.assertTrue('1111-1' in response.content)
        self.assertTrue('1992-1' in response.content)
        self.assertTrue('1111-1-a' in response.content)
