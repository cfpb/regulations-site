from unittest import TestCase

from regulations.generator.layers.location_replace import *


class LayersLocationReplaceTest(TestCase):
    def test_update_offsets_html(self):
        lr = LocationReplace()
        lr.update_offsets("a", "This is a test. It is only a test")
        self.assertEqual(lr.offsets, {0: (8, 9), 1: (27, 28)})
        lr.update_offsets("a", "This is a test. <a href='something'>link</a>")
        self.assertEqual(lr.offsets, {0: (8, 9)})

    def test_location_replace_text(self):
        lr = LocationReplace()
        replaced = lr.location_replace_text('Bunch of as as as',
                                            'as', '<sub>as</sub>', [0, 2])
        self.assertEqual('Bunch of <sub>as</sub> as <sub>as</sub>', replaced)

        lr = LocationReplace()
        replaced = lr.location_replace_text('Bunch of as as as',
                                            'as', '<sub>b</sub>', [0, 2])
        self.assertEqual('Bunch of <sub>b</sub> as <sub>b</sub>', replaced)

        lr = LocationReplace()
        replaced = lr.location_replace_text('Bunch of a_{s} a_{s} a_{s}',
                                            'a_{s}', 'a<sub>s</sub>', [0, 2])
        self.assertEqual('Bunch of a<sub>s</sub> a_{s} a<sub>s</sub>',
                         replaced)
