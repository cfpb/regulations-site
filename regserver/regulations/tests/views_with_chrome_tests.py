from unittest import TestCase

from django.conf import settings

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
