from unittest import TestCase

from regulations.generator.node_types import *

class NodeTypesTest(TestCase):
    def test_change_type_names(self):
        node_parts_before = ['1005', 'Interpretations', '3', '(b)(3)(v)']
        node_parts_after = to_markup_id(node_parts_before)
        node_string = "-".join(node_parts_after)

        self.assertEqual('I-1005-3-b3v', node_string) 
        self.assertEqual("I", node_parts_after[0])
        self.assertEqual(node_parts_before[1], "Interpretations")

    def test_change_appendix(self):
        node_parts_before = ['243', 'A', '30(a)']
        node_parts_after = to_markup_id(node_parts_before)
        node_string = "-".join(node_parts_after)

        self.assertEqual('243-A-30a', node_string)

    def test_is_appendix_not(self):
        node_parts = ['250', '5', 'A']
        self.assertFalse(is_appendix(node_parts))

    def test_transform_part_none(self):
        part = '30'
        self.assertEqual('30', transform_part(part))
