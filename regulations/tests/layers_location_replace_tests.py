from unittest import TestCase

from regulations.generator.layers.location_replace import *


class LayersLocationReplaceTest(TestCase):
    def test_update_offsets_html(self):
        lr = LocationReplace()
        lr.update_offsets("a", "This is a test. It is only a test")
        self.assertEqual(lr.offsets, {0: (8, 9), 1: (27, 28)})
        lr.update_offsets("a", "This is a test. <a href='something'>link</a>")
        self.assertEqual(lr.offsets, {0: (8, 9)})
