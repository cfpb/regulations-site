from node_types import *
from unittest import TestCase

class NodeTypesTest(TestCase):
    def test_change_type_names(self):
        node_parts_before = ['1005', 'Interpretations', '3', '(b)(3)(v)']
        node_parts_after = to_markup_id(node_parts_before)
        node_string = "-".join(node_parts_after)

        self.assertEqual('I-1005-3-b3v', node_string) 
        self.assertEqual("I", node_parts_after[0])
        self.assertEqual(node_parts_before[1], "Interpretations")
