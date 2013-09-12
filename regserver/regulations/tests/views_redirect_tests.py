from unittest import TestCase

from django.http import Http404
from django.test import RequestFactory
from mock import patch

from regulations.views.redirect import *


class ViewsRedirectTest(TestCase):
    @patch('regulations.views.redirect.ApiReader')
    def test_redirect_by_date(self, ApiReader):
        ApiReader.return_value.regversions.return_value = {'versions': [
            {'by_date': '2000-01-01', 'version': 'aaa'},
            {'by_date': '2005-05-05', 'version': 'bbb'},
            {'by_date': '2010-06-07', 'version': 'ccc'},
        ]}

        self.assertRaises(Http404, redirect_by_date, None, '8888', '1999',
                          '10', '10')
        response = redirect_by_date(None, '8888', '2000', '01', '01')
        self.assertEqual(302, response.status_code)
        self.assertTrue('aaa' in response['Location'])
        response = redirect_by_date(None, '8888', '2006', '06', '06')
        self.assertEqual(302, response.status_code)
        self.assertTrue('bbb' in response['Location'])
        response = redirect_by_date(None, '8888', '2010', '06', '08')
        self.assertEqual(302, response.status_code)
        self.assertTrue('ccc' in response['Location'])

    @patch('regulations.views.redirect.redirect_by_date')
    def test_redirect_by_get(self, redirect_by_date):
        request = RequestFactory().get('?year=2222&month=11&day=20')
        redirect_by_get(request, 'lablab')
        self.assertTrue(redirect_by_date.called)
        self.assertEqual(('lablab', '2222', '11', '20'),
                         redirect_by_date.call_args[0][1:])
