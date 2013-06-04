from api_reader import Client
import json
from mock import patch
import os
from StringIO import StringIO
import shutil
import tempfile
from unittest import TestCase

class ClientTest(TestCase):
    def setUp(self):
        self.client = Client("http://example.com")
        Client._reg_cache = {}

    def _fake_response(self, value):
        """Mock out a response -- a File-like object with encoded json"""
        return StringIO(json.dumps(value))

    @patch('api_reader.urlopen')
    def test_regulation(self, urlopen):
        to_return = {'example': 0}
        urlopen.return_value = self._fake_response(to_return)
        self.assertEqual(to_return,
                self.client.regulation("label-here", "date-here"))
        self.assertTrue(urlopen.called)
        param = urlopen.call_args[0][0]
        self.assertTrue('http://example.com' in param)
        self.assertTrue('label-here' in param)
        self.assertTrue('date-here' in param)

    @patch('api_reader.urlopen')
    def test_layer(self, urlopen):
        to_return = {'example': 1}
        urlopen.return_value = self._fake_response(to_return)
        self.assertEqual(to_return, 
                self.client.layer("layer-here", "label-here", "date-here"))
        self.assertTrue(urlopen.called)
        param = urlopen.call_args[0][0]
        self.assertTrue('http://example.com' in param)
        self.assertTrue('layer-here' in param)
        self.assertTrue('label-here' in param)
        self.assertTrue('date-here' in param)

    @patch('api_reader.urlopen')
    def test_notices(self, urlopen):
        to_return = {'example': 1}
        urlopen.return_value = self._fake_response(to_return)
        self.assertEqual(to_return, self.client.notices())
        self.assertTrue(urlopen.called)
        param = urlopen.call_args[0][0]
        self.assertTrue('http://example.com' in param)

    @patch('api_reader.urlopen')
    def test_notice(self, urlopen):
        to_return = {'example': 1}
        urlopen.return_value = self._fake_response(to_return)
        self.assertEqual(to_return, self.client.notice("doc"))
        self.assertTrue(urlopen.called)
        param = urlopen.call_args[0][0]
        self.assertTrue('http://example.com' in param)
        self.assertTrue('doc' in param)

    def test_local_fs(self):
        """Verify that it's possible to host the files locally, where
        index.html is used in place of just the directory name."""
        tmp_root = tempfile.mkdtemp() + os.sep
        notice_path = tmp_root + os.sep + "notice" + os.sep
        os.mkdir(notice_path)
        with open(notice_path + "index.html", 'w') as f:
            f.write('{"results": ["example"]}')
        client = Client(tmp_root)
        results = client.notices()
        shutil.rmtree(tmp_root)
        self.assertEqual(["example"], results['results'])

    @patch('api_reader.urlopen')
    def test_reg_cache(self, urlopen):
        child = {
            'text': 'child', 
            'children': [], 
            'label': {'text': '923-a', 'parts': ['923', 'a']}
        }
        to_return = {
            'text': 'parent', 
            'label': {'text': '923', 'parts': ['923']},
            'children': [child]
        }
        urlopen.return_value = self._fake_response(to_return)
        self.assertEqual(to_return, self.client.regulation('923', 'ver'))
        self.assertEqual(to_return, self.client.regulation('923', 'ver'))
        self.assertEqual(child, self.client.regulation('923-a', 'ver'))
        self.assertEqual(1, urlopen.call_count)
        urlopen.return_value = self._fake_response(to_return)
        self.client.regulation('923-b', 'ver')
        self.assertEqual(2, urlopen.call_count)
