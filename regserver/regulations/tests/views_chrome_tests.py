from unittest import TestCase

from django.http import HttpResponseGone
from django.test import RequestFactory
from mock import Mock, patch

from regulations.views.chrome import *
from regulations.views.error_handling import MissingContentException


class ViewsChromeTest(TestCase):
    @patch('regulations.views.error_handling.api_reader')
    @patch('regulations.views.chrome.ChromeView.set_chrome_context')
    @patch('regulations.views.chrome.generator')
    def test_404(self, generator, set_chrome_context, api_reader):
        """Test that the response of the outer view is that of the inner
        when there's an error"""
        api_reader.ApiReader.return_value.regversions.return_value = None
        generator.get_regulation.return_value = None
        generator.get_tree_paragraph.return_value = {}
        set_chrome_context.return_value = None

        class InnerView(TemplateView):
            def get(self, request, *args, **kwargs):
                return HttpResponseGone()

        class FakeView(ChromeView):
            partial_class = InnerView

        view = FakeView()
        view.request = RequestFactory().get('/')
        response = view.get(view.request, label_id='lab', version='ver')
        self.assertEqual(404, response.status_code)

    @patch('regulations.views.chrome.error_handling')
    @patch('regulations.views.chrome.ChromeView.set_chrome_context')
    @patch('regulations.views.chrome.generator')
    def test_error_propagation(self, generator, set_chrome_context, error_handling):
        """Test that the response of the outer view is that of the inner
        when there's an error"""
        error_handling.check_regulation.return_value = None
        generator.get_tree_paragraph.return_value = {}
        set_chrome_context.return_value = None

        class InnerView(TemplateView):
            def get(self, request, *args, **kwargs):
                return HttpResponseGone()

        class FakeView(ChromeView):
            partial_class = InnerView

        view = FakeView()
        view.request = RequestFactory().get('/')
        response = view.get(view.request, label_id='lab', version='ver')
        self.assertEqual(410, response.status_code)
