from unittest import TestCase
from mock import patch

from django.test import RequestFactory
from django.test.client import Client

from regulations.generator.layers.layers_applier import *
from regulations.generator.node_types import REGTEXT
from regulations.views.partial import *


class PartialParagraphViewTests(TestCase):

    @patch('regulations.views.partial.generator')
    def test_get_context_data(self, generator):
        generator.LayerCreator.return_value.get_appliers.return_value = (
            InlineLayersApplier(), ParagraphLayersApplier(),
            SearchReplaceLayersApplier())
        generator.get_tree_paragraph.return_value = {
            'text': 'Some Text',
            'children': [],
            'label': ['867', '53', 'q'],
            'node_type': REGTEXT
        }
        paragraph_id = '103-3-a'
        reg_version = '2013-10607'
        request = RequestFactory().get('/fake-path')
        view = PartialParagraphView.as_view(
            template_name='regulations/tree.html')
        response = view(request, label_id=paragraph_id, version=reg_version)
        self.assertEqual(response.context_data['node'],
                         generator.get_tree_paragraph.return_value)

    @patch('regulations.views.partial.generator')
    def test_get_404(self, generator):
        generator.get_tree_paragraph.return_value = None
        response = Client().get('/partial/202-4/ver')
        self.assertEqual(404, response.status_code)


class PartialSectionViewTests(TestCase):
    @patch('regulations.views.partial.generator')
    @patch('regulations.generator.generator.LayerCreator.get_layer_json')
    def test_get_context_data(self, get_layer_json, generator):
        get_layer_json.return_value = {'layer': 'layer'}
        generator.get_tree_paragraph.return_value = {
            'text': 'Some Text',
            'children': [],
            'label': ['205'],
            'node_type': REGTEXT
        }

        reg_part_section = '205'
        reg_version = '2013-10608'

        request = RequestFactory().get('/fake-path/?layers=meta')
        view = PartialSectionView.as_view(
            template_name='regulations/regulation-content.html')

        response = view(request, label_id=reg_part_section,
                        version=reg_version)
        root = response.context_data['tree']
        subpart = root['children'][0]
        self.assertEqual(subpart['children'][0],
                         generator.get_tree_paragraph.return_value)


class PartialViewTest(TestCase):

    def test_generate_html(self):
        regulation_tree = {'text': '', 'children': [], 'label': ['8675'],
                           'title': 'Regulation R', 'node_type': REGTEXT}
        i_applier = InlineLayersApplier()
        p_applier = ParagraphLayersApplier()
        sr_applier = SearchReplaceLayersApplier()
        appliers = (i_applier, p_applier, sr_applier)
        builder = generate_html(regulation_tree, appliers)
        self.assertEquals(builder.tree, regulation_tree)
        self.assertEquals(builder.inline_applier, i_applier)
        self.assertEquals(builder.p_applier, p_applier)
        self.assertEquals(builder.search_applier, sr_applier)
