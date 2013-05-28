from html_builder import *
from mock import Mock
from unittest import TestCase

class HTMLBuilderTest(TestCase):

    def test_process_node_appliers(self):
        node = {
            "text": "Text text text.", 
            "children": [], 
            "label": {
                "text": "123-aaa", 
                "parts": ["123", "aaa"]
            }
        }

        inline = Mock()
        inline.apply_layers.return_value = node
        par = Mock()
        par.apply_layers.return_value = node
        sr = Mock()
        sr.apply_layers.return_value = node

        builder = HTMLBuilder(inline, par, sr)
        builder.process_node(node)

        self.assertTrue(inline.apply_layers.called)
        self.assertEqual("Text text text.",
                inline.apply_layers.call_args[0][0])
        self.assertEqual("123-aaa",
                inline.apply_layers.call_args[0][1])

        self.assertTrue(par.apply_layers.called)
        self.assertEqual(node, par.apply_layers.call_args[0][0])

    def test_list_level_interpretations(self):
        builder = HTMLBuilder(None, None, None)

        parts = ['I', '101', '12', '(a)', '1']
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

