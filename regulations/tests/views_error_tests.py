from unittest import TestCase
from mock import patch

from django.http import Http404
from django.test import RequestFactory

from regulations.views import error_handling


class ErrorHandlingTest(TestCase):

    @patch('regulations.views.error_handling.api_reader')
    def test_check_regulation_none(self, api_reader):
        api_reader.ApiReader.return_value.regversions.return_value = None

        self.assertRaises(
            error_handling.MissingContentException,
            error_handling.check_regulation, '204')

    @patch('regulations.views.error_handling.api_reader')
    def test_check_regulation_exists(self, api_reader):
        api_reader.ApiReader.return_value.regversions.return_value = [1]

        result = error_handling.check_regulation('204')
        self.assertEqual(result, None)

    @patch('regulations.views.error_handling.api_reader')
    def test_check_version(self, api_reader):
        api_reader.ApiReader.return_value.regversions.return_value =\
            {'versions': [{'version': '2'}]}
        result = error_handling.check_version('204', '2')
        self.assertTrue(result)

    @patch('regulations.views.error_handling.api_reader')
    def test_check_no_version(self, api_reader):
        api_reader.ApiReader.return_value.regversions.return_value =\
            {'versions': [{'version': '3'}]}
        result = error_handling.check_version('204', '2')
        self.assertFalse(result)

    def test_handle_generic_404(self):
        request = RequestFactory().get('/fake-path')
        with self.assertRaises(Http404):
            error_handling.handle_generic_404(request)

    @patch('regulations.views.error_handling.add_to_chrome')
    @patch('regulations.views.error_handling.api_reader')
    def test_handle_missing_section_404(self, api_reader, add_to_chrome):
        api_reader.ApiReader.return_value.regversions.return_value =\
            {'versions': [{'version': '2', 'by_date':'2013-03-26'}]}
        add_to_chrome.return_value = None

        request = RequestFactory().get('/fake-path')

        extra_content = {'passed': 1, 'env': 'source'}
        response = error_handling.handle_missing_section_404(
            request, '204-1', '2', extra_content)
        self.assertEqual(response, None)
        self.assertTrue(add_to_chrome.called)
