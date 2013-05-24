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
