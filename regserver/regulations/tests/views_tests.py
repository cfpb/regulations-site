from unittest import TestCase

from mock import Mock, patch

from regulations.generator.layers.layers_applier import *
from regulations.views import *

class RegulationParagraphViewTests(TestCase):
    @patch('regulations.views.generator')
    def test_get_context_data(self, generator):
        generator.get_all_section_layers.return_value = (InlineLayersApplier(), 
                ParagraphLayersApplier(), SearchReplaceLayersApplier())
        generator.get_tree_paragraph.return_value = {
            'text': 'Some Text',
            'children': [],
            'label': {'text': '867-53-q', 'parts': ['867', '53', 'q']}
        }
        rpv = RegulationParagraphView()
        context = rpv.get_context_data(paragraph_id = '867-53-q',
            reg_version = 'verver')
        self.assertEqual(context['node'],
                generator.get_tree_paragraph.return_value)
