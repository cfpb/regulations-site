#vim: set encoding=utf-8
from unittest import TestCase
from mock import Mock

from regulations.generator.html_builder import *
from regulations.generator.layers.layers_applier import ParagraphLayersApplier
from regulations.generator.node_types import REGTEXT, APPENDIX, INTERP

class HTMLBuilderTest(TestCase):

    def test_process_node_appliers(self):
        node = {
            "text": "Text text text.", 
            "children": [], 
            "label": ["123", "aaa"],
            'node_type': REGTEXT
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
            "label": ["234", "a", "1"],
            "title": "Title (Regulation R)",
            'node_type': APPENDIX
        }
        titleless_node = {
            "title": "Title",
            'node_type': REGTEXT
        }

        parsed_title = builder.parse_doc_title(node['title'])
        no_title = builder.parse_doc_title(titleless_node['title'])

        self.assertEqual("(Regulation R)", parsed_title)
        self.assertEqual(no_title, None)

    def test_list_level_interpretations(self):
        builder = HTMLBuilder(None, None, None)

        parts = ['101', '12', 'a', 'Interp', '1']
        node_type = INTERP

        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (1, '1'))

        parts.append('j')
        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (2, 'i'))

        parts.append('B')
        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (3, 'A'))

    def test_list_level_appendices(self):
        builder = HTMLBuilder(None, None, None)

        parts = ['101', 'A', '1','a']
        node_type = APPENDIX

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
        node_type = REGTEXT

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
        node_type = REGTEXT

        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (None, None))

    def test_interp_node_with_citations(self):
        inline, p, sr = Mock(), Mock(), Mock()
        builder = HTMLBuilder(inline, p, sr)

        node = {
            'text': 'Interpretation with a link',
            'children': [],
            'node_type': INTERP,
            'label': ['999', '5', 'Interp']
        }
        p.apply_layers.return_value = node
        inline.get_layer_pairs.return_value = []
        sr.get_layer_pairs.return_value = []
        builder.process_node(node)
        layer_parameters = inline.get_layer_pairs.call_args[0]
        self.assertEqual('Interpretation with a link', layer_parameters[1])
        self.assertEqual('999-5-Interp', layer_parameters[0])

    def test_process_node_header(self):
        builder = HTMLBuilder(None, ParagraphLayersApplier(), None)
        node = {'text': '', 'children': [], 'label': ['99', '22'],
                'node_type': REGTEXT}
        builder.process_node(node)
        self.assertFalse('header' in node)

        node = {'text': '', 'children': [], 'label': ['99', '22'], 
                'title': 'Some Title', 'node_type': REGTEXT}
        builder.process_node(node)
        self.assertTrue('header' in node)
        self.assertEqual('Some Title', node['header'])
        self.assertFalse('header_marker' in node)
        self.assertFalse('header_num' in node)
        self.assertFalse('header_title' in node)

        node = {'text': '', 'children': [], 'label': ['99', '22'], 
                'title': u'§ 22.1 Title', 'node_type': REGTEXT}
        builder.process_node(node)
        self.assertTrue('header' in node)
        self.assertTrue('header_marker' in node)
        self.assertEqual(u'§&nbsp;', node['header_marker'])
        self.assertTrue('header_num' in node)
        self.assertEqual(u'22.1', node['header_num'])
        self.assertTrue('header_title' in node)
        self.assertEqual(u' Title', node['header_title'])

    def test_no_section_sign(self):
        text = HTMLBuilder.section_sign_hard_space(' abc')
        self.assertEquals(text, ' abc')
        self.assertTrue(True)
