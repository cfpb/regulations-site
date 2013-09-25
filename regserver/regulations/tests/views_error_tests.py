from unittest import TestCase
from mock import patch

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
