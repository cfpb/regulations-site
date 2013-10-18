from unittest import TestCase

from mock import patch

from regulations.views.partial_sxs import *
from regulations.generator.layers.utils import convert_to_python


class ParagrasphSXSViewTests(TestCase):
    @patch('regulations.views.partial_sxs.api_reader')
    def test_further_analyses(self, api_reader):
        doc1 = {'publication_date': '2009-04-05', 'fr_volume': 21,
                'fr_page': 98989, 'reference': ['doc1', '1212-31']}
        doc2 = {'publication_date': '2010-03-03', 'fr_volume': 22,
                'fr_page': 87655, 'reference': ['doc2', '1212-31']}
        doc3 = {'publication_date': '2010-10-12', 'fr_volume': 22,
                'fr_page': 90123, 'reference': ['doc3', '1212-31']}
        doc4 = {'publication_date': '2009-03-07', 'fr_volume': 21,
                'fr_page': 98888, 'reference': ['doc4', '1212-31-b']}
        api_reader.ApiReader.return_value.layer.return_value = {
            '1212-31': [doc1, doc2, doc3],
            '1212-31-b': [doc4]
        }

        psv = ParagraphSXSView()
        self.assertEqual(psv.further_analyses('1212-31', 'doc1', 'v1'),
            convert_to_python([doc3, doc2]))
        self.assertEqual(psv.further_analyses('1212-31', 'doc5', 'v1'),
            convert_to_python([doc3, doc2, doc1]))
        self.assertEqual(psv.further_analyses('1212-31', 'doc3', 'v1'),
            convert_to_python([doc2, doc1]))

        self.assertEqual(psv.further_analyses('1212-31-b', 'doc3', 'v1'),
            convert_to_python([doc4]))
        self.assertEqual(psv.further_analyses('1212-31-b', 'doc4', 'v1'),
            [])

        self.assertEqual(psv.further_analyses('1212-31-c', 'doc1', 'v1'),
            [])
