from datetime import datetime, timedelta
from unittest import TestCase

from mock import patch

from regulations.generator.versions import *


class VersionsTest(TestCase):
    @patch('regulations.generator.versions.api_reader')
    def test_fetch_grouped_history(self, reader):
        client = reader.ApiReader.return_value

        future = datetime.today() + timedelta(days=5)
        future = future.strftime('%Y-%m-%d')
        client.regversions.return_value = {'versions': [
            {'by_date': '2001-01-01', 'version': 'v1'},
            {'versions': 'v2'},
            {'by_date': '2003-03-03', 'version': 'v3'},
            {'versions': 'v4'},
            {'versions': 'v5'},
            {'by_date': future, 'version': 'v6'},
        ]}

        n1 = {'effective_on': '2001-01-01', 
                'publication_date': '2000-10-10', 
                'fr_url': 'http://n1'}
        n2 = {'effective_on': '2003-03-03', 
                'publication_date': '2001-01-01', 
                'fr_url': 'http://n2'}
        n3 = {'effective_on': '2003-03-03', 
                'publication_date': '2002-02-02', 
                'fr_url': 'http://n3'}
        n4 = {'effective_on': future, 
                'publication_date': '2005-05-05',
                'fr_url': 'http://n4'}
        n5 = {'effective_on': future, 
                'publication_date': '2005-06-05',
                'fr_url': 'http://n5'}
        n6 = {'effective_on': future, 
                'publication_date': '2005-07-05',
                'fr_url': 'http://n6'}
        n6_1 = {'effective_on': future, 
                'publication_date': '2005-07-05',
                'fr_url': 'http://n6'}
        client.notices.return_value = {
                'results': [n1, n2, n3, n5, n4, n6, n6_1]}

        history = fetch_grouped_history('111')
        self.assertEqual(3, len(history))
        v1, v2, v3 = history

        self.assertEqual('future', v1['timeline'])
        self.assertEqual('current', v2['timeline'])
        self.assertEqual('past', v3['timeline'])

        # n6_1 should NOT be present in this list
        self.assertEqual(convert_to_python([n6, n5, n4]), v1['notices'])
        self.assertEqual(convert_to_python([n3, n2]), v2['notices'])
        self.assertEqual(convert_to_python([n1]), v3['notices'])
