from unittest import TestCase

from mock import patch
from django.http import Http404
from django.test import RequestFactory

from regulations.generator.layers.layers_applier import (
    InlineLayersApplier, ParagraphLayersApplier, SearchReplaceLayersApplier)
from regulations.generator.node_types import INTERP
from regulations.views import partial_interp


class PartialInterpViewTest(TestCase):
    @patch('regulations.views.partial.generator')
    def test_get_context_data(self, generator):
        generator.LayerCreator.return_value.get_appliers.return_value = (
            InlineLayersApplier(), ParagraphLayersApplier(),
            SearchReplaceLayersApplier())
        generator.get_tree_paragraph.return_value = {
            'text': 'Some Text',
            'children': [],
            'label': ['867', '53', 'q', 'Interp'],
            'node_type': INTERP
        }
        request = RequestFactory().get('/fake-path')
        view = partial_interp.PartialInterpView.as_view()
        response = view(request, label_id='lablab', version='verver')
        self.assertEqual(response.context_data['c']['node_type'], INTERP)
        self.assertEqual(response.context_data['c']['children'],
                         [generator.get_tree_paragraph.return_value])
        self.assertFalse(response.context_data['inline'])

        view = partial_interp.PartialInterpView.as_view(inline=True)
        response = view(request, label_id='lablab', version='verver')
        self.assertEqual(response.context_data['c']['node_type'], INTERP)
        self.assertEqual(response.context_data['c']['children'],
                         [generator.get_tree_paragraph.return_value])
        self.assertTrue(response.context_data['inline'])


class PartialSubterpViewTest(TestCase):
    @patch('regulations.views.partial_interp.generator')
    @patch('regulations.views.partial_interp.utils')
    @patch('regulations.views.partial_interp.generate_html')
    def test_get_context_data(self, genhtml, utils, generator):
        generator.get_tree_paragraph.return_value = None
        utils.subterp_expansion.return_value = []

        request = RequestFactory().get('/fake-path')
        view = partial_interp.PartialSubterpView.as_view()
        try:
            response = view(request, label_id='lablab', version='verver')
            self.assertTrue(False)
        except Http404:
            pass

        utils.subterp_expansion.return_value = ["sec1", "sec2", "sec3"]
        view(request, label_id='lablab', version='verver')
        self.assertEqual(3, generator.get_tree_paragraph.call_count)
        call1, call2, call3 = generator.get_tree_paragraph.call_args_list
        self.assertEqual(('sec1', 'verver'), call1[0])
        self.assertEqual(('sec2', 'verver'), call2[0])
        self.assertEqual(('sec3', 'verver'), call3[0])
