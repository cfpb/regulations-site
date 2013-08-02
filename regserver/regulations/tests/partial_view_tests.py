from unittest import TestCase
from mock import Mock, patch

from django.test import RequestFactory

from regulations.generator.layers.layers_applier import *
from regulations.views.partial import *

class PartialParagraphViewTests(TestCase):

    @patch('regulations.views.partial.generator')
    def test_get_context_data(self, generator):
        generator.get_all_section_layers.return_value = (InlineLayersApplier(), 
                ParagraphLayersApplier(), SearchReplaceLayersApplier())
        generator.get_tree_paragraph.return_value = {
            'text': 'Some Text',
            'children': [],
            'label': ['867', '53', 'q']
        }
        paragraph_id = '103-3-a'
        reg_version = '2013-10607'
        request = RequestFactory().get('/fake-path')
        view = PartialParagraphView.as_view(template_name='tree.html')
        response = view(request, paragraph_id=paragraph_id, reg_version=reg_version)
        self.assertEqual(response.context_data['node'], 
            generator.get_tree_paragraph.return_value)


class PartialSectionViewTests(TestCase):
    @patch('regulations.views.partial.generator')
    @patch('regulations.generator.generator.LayerCreator.get_layer_json')
    def test_get_context_data(self, get_layer_json, generator):
        get_layer_json.return_value = {'layer':'layer'}
        generator.get_tree_paragraph.return_value = {
            'text': 'Some Text',
            'children': [],
            'label': {'text': '205', 'parts': ['205']}
        }

        reg_part_section = '205'
        reg_version = '2013-10608'

        request = RequestFactory().get('/fake-path/?layers=meta')
        view = PartialSectionView.as_view(template_name='regulation-content.html')

        response = view(request, 
                    reg_part_section=reg_part_section,
                    reg_version=reg_version)
        self.assertEqual(response.context_data['tree'], 
            generator.get_tree_paragraph.return_value)
