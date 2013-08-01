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
            'label': {'text': '867-53-q', 'parts': ['867', '53', 'q']}
        }
        paragraph_id = '103-3-a'
        reg_version = '2013-10607'
        request = RequestFactory().get('/fake-path')
        view = PartialParagraphView.as_view(template_name='tree.html')
        response = view(request, paragraph_id=paragraph_id, reg_version=reg_version)
        self.assertEqual(response.context_data['node'], 
            generator.get_tree_paragraph.return_value)
