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

    def test_add_extras(self):
        view = ChromeView()
        context = {}
        view.add_extras(context)

        self.assertTrue('GOOGLE_ANALYTICS_ID' in context)
        self.assertTrue('GOOGLE_ANALYTICS_SITE' in context)
        self.assertTrue('env' in context)

    def test_add_extras_env(self):
        view = ChromeView()
        context = {}
        
        settings.DEBUG = True
        view.add_extras(context)
        self.assertEqual('source', context['env'])

        settings.DEBUG = False
        view.add_extras(context)
        self.assertEqual('built', context['env'])

    @patch('regulations.generator.generator')
    def test_get_404(self, generator):
        generator.get_regulation.return_value = None
        response = Client().get('/regulation/111/222')
        self.assertEqual(404, response.status_code)

    @patch('regulations.generator.generator')
    def test_get_404_tree(self, generator):
        generator.get_regulation.return_value = {'regulation':'tree'}
        generator.get_tree_paragraph.return_value = None
        response = Client().get('/regulation/111/222')
        self.assertEqual(404, response.status_code)
