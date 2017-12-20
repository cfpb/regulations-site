import os
import shutil
import tempfile

from django.conf import settings
from django.test import TestCase, override_settings

from regulations.generator.api_client import ApiClient


class ClientTest(TestCase):
    def test_local_filesystem(self):
        """ Verify that it's possible to host the files locally, where
        index.html is used in place of just the directory name. """
        tmp_root = tempfile.mkdtemp() + os.sep
        notice_path = tmp_root + os.sep + "notice" + os.sep
        os.mkdir(notice_path)
        with open(notice_path + "index.html", 'w') as f:
            f.write('{"results": ["example"]}')
        client = ApiClient()
        client.base_url = tmp_root
        results = client.get('notice')
        shutil.rmtree(tmp_root)
        self.assertEqual(["example"], results['results'])


@override_settings(EREGS_REGCORE_URLS='regulations.tests.mock_regcore_urls')
class ClientUsingRegCoreTests(TestCase):
    @override_settings()
    def test_no_setting_doesnt_set_regcore_urls(self):
        del settings.EREGS_REGCORE_URLS
        self.assertIsNone(ApiClient().regcore_urls)

    @override_settings(EREGS_REGCORE_URLS='this.does.not.exist')
    def test_invalid_setting_raises_import_error(self):
        with self.assertRaises(ImportError):
            ApiClient()

    def test_valid_setting_sets_regcore_urls(self):
        self.assertEqual(
            ApiClient().regcore_urls.__name__,
            'regulations.tests.mock_regcore_urls'
        )

    def test_valid_request_returns_content(self):
        self.assertEqual(ApiClient().get('returns-200'), {'foo': 'bar'})

    def test_valid_request_passes_params(self):
        self.assertEqual(
            ApiClient().get('returns-get', params={'zap': 'boom'}),
            {'zap': 'boom'}
        )

    def test_request_returning_404_returns_none(self):
        self.assertIsNone(ApiClient().get('returns-404'))

    def test_request_raising_http404_returns_none(self):
        self.assertIsNone(ApiClient().get('raises-http404'))

    def test_request_raising_exception_returns_that_exception(self):
        with self.assertRaises(RuntimeError):
            ApiClient().get('raises-exception')

    def test_unresolvable_request_returns_none(self):
        self.assertIsNone(ApiClient().get('this-doesnt-resolve'))
