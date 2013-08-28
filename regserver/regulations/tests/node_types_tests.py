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

    def test_is_appendix(self):
        node_parts = ['250', 'A']
        self.assertTrue(is_appendix(node_parts))

    def test_transform_part_none(self):
        part = '30'
        self.assertEqual('30', transform_part(part))

    def test_label_to_text(self):
        self.assertEqual('2323.4', label_to_text(['2323', '4']))
        self.assertEqual('2323.5(r)(3)',
                         label_to_text(['2323', '5', 'r', '3']))
        self.assertEqual('Appendix A', label_to_text(['2323', 'A']))
        self.assertEqual('Appendix A-4', label_to_text(['2323', 'A', '4']))
        self.assertEqual('Appendix A-4(b)(2)',
                         label_to_text(['2323', 'A', '4', 'b', '2']))
        self.assertEqual('Comment for 2323.5',
                         label_to_text(['2323', '5', 'Interp']))
        self.assertEqual('Comment for 2323.7(b)-1.v',
                         label_to_text(['2323', '7', 'b', 'Interp', '1', 'v']))
        self.assertEqual('Comment for Appendix Z',
                         label_to_text(['2323', 'Z', 'Interp']))
