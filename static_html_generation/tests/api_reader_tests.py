from api_reader import Client
import json
from mock import patch
from StringIO import StringIO
from unittest import TestCase

class ClientTest(TestCase):
    def setUp(self):
        self.client = Client("http://example.com")

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
