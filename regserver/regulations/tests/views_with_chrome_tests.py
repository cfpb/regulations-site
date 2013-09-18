from unittest import TestCase

from django.conf import settings
from django.test.client import Client
from mock import patch

from regulations.views.chrome import ChromeView

class ViewTests(TestCase):
    def setUp(self):
        self.original_debug = settings.DEBUG

    def tearDown(self):
        settings.DEBUG = self.original_debug

    @patch('regulations.views.chrome.generator')
    def test_get_404(self, generator):
        generator.get_regulation.return_value = None
        response = Client().get('/regulation/111/222')
        self.assertEqual(404, response.status_code)

    @patch('regulations.views.chrome.generator')
    def test_get_404_tree(self, generator):
        generator.get_regulation.return_value = {'regulation':'tree'}
        generator.get_tree_paragraph.return_value = None
        response = Client().get('/regulation/111/222')
        self.assertEqual(404, response.status_code)
