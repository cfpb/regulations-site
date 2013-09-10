from unittest import TestCase

from mock import patch
from django.test.client import Client
from django.test import RequestFactory

from regulations.generator.node_types import REGTEXT
from regulations.generator.layers.diff_applier import DiffApplier
from regulations.generator.layers.layers_applier import InlineLayersApplier
from regulations.generator.layers.layers_applier import ParagraphLayersApplier
from regulations.generator.layers.layers_applier import SearchReplaceLayersApplier

from regulations.views.diff import PartialSectionDiffView, get_appliers


class PartialSectionDiffViewTest(TestCase):
    @patch('regulations.views.diff.generator')
    def test_get_appliers(self, generator):
        diff_applier = DiffApplier({'some': 'diff'}, None)
        generator.get_diff_applier.return_value = diff_applier
        #diff_view = PartialSectionDiffView()
        _, _, _, da = get_appliers('204-2', '1', '2')
        self.assertEqual(da, diff_applier)

    @patch('regulations.views.diff.generator')
    def test_get_404(self, generator):
        generator.get_tree_paragraph.return_value = None
        response = Client().get('/partial/diff/111/222')
        self.assertEqual(404, response.status_code)

    @patch('regulations.views.diff.utils')
    @patch('regulations.views.diff.generator')
    def test_get_context_data(self, generator, utils):
        diff_applier = DiffApplier({'204-3': {'op':'modified'}}, '204-3')
        generator.get_diff_applier.return_value = diff_applier
        generator.get_tree_paragraph.return_value = {
            'text': 'Some Text',
            'children': [],
            'label_id':'204-3',
            'label': ['204', '3'],
            'node_type': REGTEXT}
        utils.handle_specified_layers.return_value = ( 
            InlineLayersApplier(),
            ParagraphLayersApplier(),
            SearchReplaceLayersApplier())
        request = RequestFactory().get('/fake-path')
        view = PartialSectionDiffView.as_view(
            template_name='regulation-content.html')
        view(request, label_id='204-3', version='2', newer_version='3')
        self.assertTrue(generator.get_diff_applier.called)
