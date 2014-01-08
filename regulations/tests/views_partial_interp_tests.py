from unittest import TestCase

from mock import patch
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
