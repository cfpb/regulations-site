from unittest import TestCase

from django.http import HttpResponseGone
from django.test import RequestFactory
from mock import patch

from regulations.views.chrome import *


class ViewsChromeTest(TestCase):
    @patch('regulations.views.error_handling.api_reader')
    @patch('regulations.views.chrome.ChromeView.set_chrome_context')
    @patch('regulations.views.chrome.generator')
    def test_404(self, generator, set_chrome_context, api_reader):
        """Test that the response of the outer view is that of the inner
        when there's an error"""
        api_reader.ApiReader.return_value.regversions.return_value = None
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
    @patch('regulations.views.chrome.generator')
    @patch('regulations.views.chrome.SideBarView')
    def test_error_propagation(self, sbv, generator, error_handling):
        """While we don't rely on this sort of propagation for the main
        content (much), test it in the sidebar"""
        sbv.as_view.return_value.return_value = HttpResponseGone()
        
        class FakeView(ChromeView):
            def add_main_content(self, context):
                pass
            def set_chrome_context(self, context, reg_part, version):
                pass

        view = FakeView()
        view.request = RequestFactory().get('/')
        response = view.get(view.request, label_id='lab', version='ver')
        self.assertEqual(410, response.status_code)
