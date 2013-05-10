from node_types import NodeTypes
from unittest import TestCase

class NodeTypesTest(TestCase):
    def test_change_type_names(self):
        self.node_types = NodeTypes()

        node_parts_before = ['1005', 'Interpretations', '3', '(b)']
        node_parts_after = self.node_types.change_type_names(node_parts_before)
        node_string = "-".join(node_parts_after)

        self.assertEqual('I-1005-3-(b)', node_string) 
        self.assertEqual("I", node_parts_after[0])
