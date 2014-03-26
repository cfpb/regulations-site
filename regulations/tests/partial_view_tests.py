from unittest import TestCase
from mock import Mock, patch

from django.test import RequestFactory
from django.test.client import Client

from regulations.generator.layers.layers_applier import *
from regulations.generator.node_types import EMPTYPART, INTERP, REGTEXT
from regulations.views.partial import *


class PartialParagraphViewTests(TestCase):
    @patch.object(PartialParagraphView, 'section_navigation')
    def test_transform_context(self, sn):
        ppv = PartialParagraphView()
        builder = Mock()
        builder.tree = {'label': ['1111', '22', 'a', '5'],
                        'node_type': REGTEXT}
        ctx = {'label_id': '1111-22-a-5-i', 'version': 'vvvv'}
        ppv.transform_context(ctx, builder)
        self.assertEqual(ctx['tree'], {
            'node_type': REGTEXT, 'label': ['1111'],
            'children': [{
                'node_type': EMPTYPART, 'label': ['1111', 'Subpart'],
                'children': [{
                    'node_type': REGTEXT, 'label': ['1111', '22'],
                    'markup_id': '1111-22-a-5-i',
                    'children': [{
                        'node_type': REGTEXT, 'label': ['1111', '22', 'a'],
                        'children': [builder.tree]}]}]}]})

        builder.tree = {'label': ['1111', 'Interp', 'h1'],
                        'node_type': INTERP}
        ctx = {'label_id': '1111-Interp-h1', 'version': 'vvvv'}
        ppv.transform_context(ctx, builder)
        self.assertEqual(ctx['tree'], {
            'node_type': REGTEXT, 'label': ['1111'],
            'children': [{
                'node_type': INTERP, 'label': ['1111', 'Interp'],
                'markup_id': '1111-Interp-h1',
                'children': [builder.tree]}]})


class PartialSectionViewTests(TestCase):
    @patch('regulations.views.partial.generator')
    @patch('regulations.views.partial.navigation')
    @patch('regulations.generator.generator.LayerCreator.get_layer_json')
    def test_get_context_data(self, get_layer_json, navigation, generator):
        get_layer_json.return_value = {'layer': 'layer'}
        navigation.nav_sections.return_value = None, None
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
