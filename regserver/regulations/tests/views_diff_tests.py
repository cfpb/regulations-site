from unittest import TestCase

from mock import patch
from django.test.client import Client
from django.test import RequestFactory

from regulations.generator.node_types import REGTEXT
from regulations.generator.layers.diff_applier import DiffApplier
from regulations.views.diff import PartialSectionDiffView


class PartialSectionDiffViewTest(TestCase):
    @patch('regulations.views.diff.generator')
    def test_get_appliers(self, generator):
        diff_applier = DiffApplier({'some': 'diff'})
        generator.get_diff_applier.return_value = diff_applier
        diff_view = PartialSectionDiffView()
        _, _, _, da = diff_view.get_appliers('204-2', '1', '2')
        self.assertEqual(da, diff_applier)

    @patch('regulations.views.diff.generator')
    def test_get_404(self, generator):
        generator.get_tree_paragraph.return_value = None
        response = Client().get('/partial/diff/111/222')
        self.assertEqual(404, response.status_code)

    @patch('regulations.views.diff.generator')
    def test_get_context_data(self, generator):
        diff_applier = DiffApplier({'some': 'diff'})
        generator.get_diff_applier.return_value = diff_applier
        generator.get_tree_paragraph.return_value = {
            'text': 'Some Text',
            'children': [],
            'label': ['204', '3', 'q'],
            'node_type': REGTEXT}
        request = RequestFactory().get('/fake-path')
        view = PartialSectionDiffView.as_view(
            template_name='regulation-content.html')
        view(request, label_id='204-3', version='2', newer_version='3')
        self.assertTrue(generator.get_diff_applier.called)
