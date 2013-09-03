import re
from unittest import TestCase

from mock import patch

from django.test.client import Client


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
        response = Client().get('/partial/sidebar/1111-7/verver')
        self.assertTrue(bool(re.search(r'\b7\b', response.content)))
        self.assertTrue('7(a)' in response.content)
        self.assertTrue('1992-2' in response.content)
        self.assertTrue('1111-7' in response.content)
        self.assertTrue('1992-1' in response.content)
        self.assertTrue('1111-7-a' in response.content)

    @patch('regulations.views.sidebar.api_reader')
    def test_get_404(self, api_reader):
        api_reader.ApiReader.return_value.layer.return_value = None
        response = Client().get('/partial/sidebar/1111-2/verver')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(api_reader.ApiReader.return_value.layer.called)
