from unittest import TestCase
from mock import patch
from django.test import RequestFactory
from django.test.client import Client

from regulations.views.chrome_breakaway import *

class ChromeSXSViewTests(TestCase):

    @patch('regulations.views.chrome_breakaway.api_reader')
    @patch('regulations.views.chrome_breakaway.ChromeSXSView.content')
    def test_get(self, content, api_reader):
        content.return_value = ''
        api_reader.ApiReader.return_value.layer.return_value = {
            '204':[''],
        }
        request = RequestFactory().get('/fake-path/204-2/2013-1?from_version=2014-2')

        view = ChromeSXSView.as_view(template_name='regulations/breakaway-chrome.html')
        response = view(
            request, label_id='204-2', from_version='2014-2', notice_id='2013-1')

        self.assertEqual(response.context_data['reg_part'], '204')
