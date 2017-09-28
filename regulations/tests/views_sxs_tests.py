from unittest import TestCase

from django.template import Template
from django.test import RequestFactory
from mock import patch

from regulations.views import error_handling
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
        self.assertEqual(
            psv.further_analyses('1212-31', 'doc1', 'v1', 98989),
            convert_to_python([doc3, doc2]))
        self.assertEqual(
            psv.further_analyses('1212-31', 'doc5', 'v1', 0),
            convert_to_python([doc3, doc2, doc1]))
        self.assertEqual(
            psv.further_analyses('1212-31', 'doc3', 'v1', 90123),
            convert_to_python([doc2, doc1]))

        self.assertEqual(
            psv.further_analyses('1212-31-b', 'doc3', 'v1', 90123),
            convert_to_python([doc4]))
        self.assertEqual(psv.further_analyses('1212-31-b', 'doc4',
                                              'v1', 98888), [])
        self.assertEqual(psv.further_analyses('1212-31-c', 'doc1', 
                                              'v1', 98989), [])

        # Same notice + label. Different page
        doc5 = {'publication_date': '2009-04-05', 'fr_volume': 21,
                'fr_page': 10101, 'reference': ['doc1', '1212-31']}
        api_reader.ApiReader.return_value.layer.return_value = {
            '1212-31': [doc1, doc2, doc3, doc5],
            '1212-31-b': [doc4]
        }
        self.assertEqual(
            psv.further_analyses('1212-31', 'doc1', 'v1', 98989),
            convert_to_python([doc5, doc3, doc2]))
        self.assertEqual(
            psv.further_analyses('1212-31', 'doc1', 'v1', 10101),
            convert_to_python([doc3, doc2, doc1]))
        self.assertEqual(
            psv.further_analyses('1212-31', 'doc3', 'v1', 90123),
            convert_to_python([doc5, doc2, doc1]))

    def test_footnotes(self):
        psv = ParagraphSXSView()
        notice = {'footnotes': {
            '12': 'Twelve',
            '22': 'Twenty-two',
            '31': 'Thirty-one',
            '45': 'Forty-five'
        }}
        sxs = {
            'footnote_refs': [
                {'reference': '12', 'paragraph': 4, 'offset': 233},
                {'reference': '22', 'paragraph': 2, 'offset': 111}],
            'children': [
                {'footnote_refs': [
                    {'reference': '45', 'paragraph': 3, 'offset': 22}],
                 'children': []}]}
        footnotes = psv.footnotes(notice, sxs)
        self.assertEqual(len(footnotes), 3)
        self.assertEqual(footnotes[0]['reference'], '12')
        self.assertEqual(footnotes[0]['text'], 'Twelve')
        self.assertEqual(footnotes[1]['reference'], '22')
        self.assertEqual(footnotes[1]['text'], 'Twenty-two')
        self.assertEqual(footnotes[2]['reference'], '45')
        self.assertEqual(footnotes[2]['text'], 'Forty-five')

    def test_footnote_refs(self):
        psv = ParagraphSXSView()
        psv.footnote_tpl = Template("[{{footnote.reference}}]")
        sxs = {
            'paragraphs': [
                'This is paragraph 1, I mean zero',
                'Will the real paragraph one please stand up?',
                'I am paragraph 10. Is that good enough?'],
            'footnote_refs': [
                {'reference': '1', 'paragraph': 0, 'offset': 7},
                {'reference': '2', 'paragraph': 0, 'offset': 27},
                {'reference': '12', 'paragraph': 2, 'offset': 1}],
            'children': [
                {'paragraphs': ['Subparagraph here'],
                 'footnote_refs': [
                     {'reference': '22', 'paragraph': 0, 'offset': 12}],
                 'children': []}]}
        psv.footnote_refs(sxs)
        self.assertEqual('This is[1] paragraph 1, I mean[2] zero',
                         sxs['paragraphs'][0])
        self.assertEqual('Will the real paragraph one please stand up?',
                         sxs['paragraphs'][1])
        self.assertEqual('I[12] am paragraph 10. Is that good enough?',
                         sxs['paragraphs'][2])
        self.assertEqual('Subparagraph[22] here',
                         sxs['children'][0]['paragraphs'][0])

    @patch('regulations.views.partial_sxs.generator')
    @patch('regulations.views.partial_sxs.notices')
    @patch.object(ParagraphSXSView, 'further_analyses')
    def test_get_context_data(self, further_analyses, notices, generator):
        psv = ParagraphSXSView()
        generator.get_notice_and_sxs.return_value = ({}, {
            'labels': ['lablab', 'another-label'],
            'children': [],
            'page': 1234,
            'paragraphs': ['some', 'content']
        })
        context = psv.get_context_data(label_id='lablab', notice_id='nnnn',
                                       version='vvv')
        self.assertTrue('sxs' in context)
        self.assertTrue('label' in context['sxs'])

    @patch('regulations.views.partial_sxs.generator')
    @patch('regulations.views.partial_sxs.notices')
    @patch.object(ParagraphSXSView, 'further_analyses')
    def test_get_context_data_notice_id_fallback(self, further_analyses, 
            notices, generator):
        """ If the version number fails, try to fetch by notice_id """
        psv = ParagraphSXSView()
        generator.get_notice_and_sxs.side_effect = [(None, None), ({}, {
            'labels': ['lablab', 'another-label'],
            'children': [],
            'page': 1234,
            'paragraphs': ['some', 'content']
        })]
        context = psv.get_context_data(label_id='lablab', notice_id='nnnn',
                                       version='vvv')

        # Should be called twice
        self.assertEqual(generator.get_notice_and_sxs.call_count, 2)

        # Once with version
        self.assertEqual(generator.get_notice_and_sxs.call_args_list[0][0][1],
                'vvv')

        # Once with notice
        self.assertEqual(generator.get_notice_and_sxs.call_args_list[1][0][1],
                'nnnn')

        self.assertTrue('sxs' in context)
        self.assertTrue('label' in context['sxs'])

    @patch(
        'regulations.views.partial_sxs.ParagraphSXSView.get_context_data',
        side_effect=error_handling.MissingContentException
    )
    def test_missing_content_raises_404(self, get_context_data):
        with self.assertRaises(Http404):
            request = RequestFactory().get('/partial/sxs/1005-31-a/2012-1728')
            ParagraphSXSView.as_view()(
                request,
                label_id='1005-31-a',
                notice_id='2012-1728'
            )
