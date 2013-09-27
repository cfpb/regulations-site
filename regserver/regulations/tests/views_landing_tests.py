from unittest import TestCase
from mock import patch

from regulations.views import landing


class LandingViewTest(TestCase):
    
    @patch('regulations.views.landing.api_reader')
    def test_regulation_exists_not(self, api_reader):
        api_reader.ApiReader.return_value.regversions.return_value = None
        reg_versions = landing.regulation_exists('204')
        self.assertFalse(reg_versions)

    @patch('regulations.views.landing.api_reader')
    def test_regulation_exists_not(self, api_reader):
        api_reader.ApiReader.return_value.regversions.return_value = [{'version':'exists'}]
        reg_versions = landing.regulation_exists('204')
        self.assertTrue(reg_versions)

    @patch('regulations.views.landing.fetch_grouped_history')
    def test_get_versions(self, fetch_grouped_history):
        fetch_grouped_history.return_value = [
            {'timeline': 'future', 'version': 'a'}, 
            {'timeline': 'current', 'version': 'b'}]
        current_ver, next_ver = landing.get_versions('204')
        self.assertEqual({'timeline': 'current', 'version': 'b'}, current_ver)
        self.assertEqual({'timeline': 'future', 'version': 'a'}, next_ver)

    @patch('regulations.views.landing.fetch_grouped_history')
    def test_get_versions_no_next(self, fetch_grouped_history):
        fetch_grouped_history.return_value = [
            {'timeline': 'current', 'version': 'b'}]
        current_ver, next_ver = landing.get_versions('204')
        self.assertEqual({'timeline': 'current', 'version': 'b'}, current_ver)
        self.assertEqual(None, next_ver)
