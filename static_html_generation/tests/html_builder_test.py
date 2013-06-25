#vim: set encoding=utf-8
from html_builder import *
from layers.layers_applier import ParagraphLayersApplier
from mock import Mock
from unittest import TestCase

class HTMLBuilderTest(TestCase):

    def test_process_node_appliers(self):
        node = {
            "text": "Text text text.", 
            "children": [], 
            "label": {
                "text": "123-aaa", 
                "parts": ["123", "aaa"],
            }
        }

        inline = Mock()
        inline.get_layer_pairs.return_value = []
        par = Mock()
        par.apply_layers.return_value = node
        sr = Mock()
        sr.get_layer_pairs.return_value = []

        builder = HTMLBuilder(inline, par, sr)
        builder.process_node(node)

        self.assertTrue(inline.get_layer_pairs.called)
        self.assertEqual("123-aaa",
                inline.get_layer_pairs.call_args[0][0])
        self.assertEqual("Text text text.",
                inline.get_layer_pairs.call_args[0][1])

        self.assertTrue(par.apply_layers.called)
        self.assertEqual(node, par.apply_layers.call_args[0][0])

    def test_header_parsing(self):
        builder = HTMLBuilder(None, None, None)

        node = {
            "label": {
                "parts": ["234", "a", "1"],
                "title": "Title (Regulation R)"
            }
        }
        titleless_node = {
            "label": {
                "title": "Title"
            }
        }

        parsed_title = builder.parse_doc_title(node['label']['title'])
        no_title = builder.parse_doc_title(titleless_node['label']['title'])

        self.assertEqual("(Regulation R)", parsed_title)
        self.assertEqual(no_title, None)

    def test_list_level_interpretations(self):
        builder = HTMLBuilder(None, None, None)

        parts = ['I', '101', '12(a)', '1']
        node_type = 'interpretation'

        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (1, '1'))

        parts.append('(j)')
        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (2, 'i'))

        parts.append('B')
        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (3, 'A'))

    def test_list_level_appendices(self):
        builder = HTMLBuilder(None, None, None)

        parts = ['101', 'A', '1','a']
        node_type = 'appendix'

        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (1, 'a'))

        parts.append('2')
        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (2, '1'))

        parts.append('k')
        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (3, 'i'))

        parts.append('B')
        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (4, 'A'))

    def test_list_level_regulations(self):
        builder = HTMLBuilder(None, None, None)

        parts = ['101','1','a']
        node_type = 'regulation'

        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (1, 'a'))

        parts.append('2')
        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (2, '1'))

        parts.append('k')
        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (3, 'i'))

        parts.append('B')
        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (4, 'A'))

    def test_list_level_regulations_no_level(self):
        builder = HTMLBuilder(None, None, None)

        parts = ['101','1']
        node_type = 'regulation'

        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (None, None))

    def test_interp_node_with_citations(self):
        inline, p, sr = Mock(), Mock(), Mock()
        builder = HTMLBuilder(inline, p, sr)

        node = {
            'text': 'Interpretation with a link',
            'children': [],
            'label': {
                'text': '999-Interpretations-5', 
                'parts': ['999', 'Interpretations', '5']
            }
        }
        p.apply_layers.return_value = node
        inline.get_layer_pairs.return_value = []
        sr.get_layer_pairs.return_value = []
        builder.process_node(node)
        layer_parameters = inline.get_layer_pairs.call_args[0]
        self.assertEqual('Interpretation with a link', layer_parameters[1])
        self.assertEqual('999-Interpretations-5', layer_parameters[0])

    def test_process_node_header(self):
        builder = HTMLBuilder(None, ParagraphLayersApplier(), None)
        node = {'text': '', 'children': [], 'label': {
            'text': '99-22', 'parts': ['99', '22']}}
        builder.process_node(node)
        self.assertFalse('header' in node)

        node = {'text': '', 'children': [], 'label': {
            'text': '99-22', 'parts': ['99', '22'], 'title': 'Some Title'}}
        builder.process_node(node)
        self.assertTrue('header' in node)
        self.assertEqual('Some Title', node['header'])
        self.assertFalse('header_marker' in node)
        self.assertFalse('header_num' in node)
        self.assertFalse('header_title' in node)

        node = {'text': '', 'children': [], 'label': {
            'text': '99-22', 'parts': ['99', '22'], 
            'title': u'§ 22.1 Title'}}
        builder.process_node(node)
        self.assertTrue('header' in node)
        self.assertEqual(node['label']['title'], node['header'])
        self.assertTrue('header_marker' in node)
        self.assertEqual(u'§', node['header_marker'])
        self.assertTrue('header_num' in node)
        self.assertEqual(u' 22.1', node['header_num'])
        self.assertTrue('header_title' in node)
        self.assertEqual(u' Title', node['header_title'])
