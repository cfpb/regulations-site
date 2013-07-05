from regulations.generator.layers.analyses import *
from unittest import TestCase

class SectionBySectionLayerTest(TestCase):

    def test_apply_layer(self):
        layer = {
            "111-22": [{
                "reference": ["2009-22", "111-22"],
                "text": "Newer analysis"
            }, {
                "reference": ["2007-11", "111-22"],
                "text": "Older analysis"
            }],
            "111-22-a": [{
                "reference": ["2009-22", "111-22-a"],
                "text": "Paragraph analysis"
            }]
        }
        sxs = SectionBySectionLayer(layer)
        
        key, value = sxs.apply_layer("111-22")
        self.assertEqual("analyses", key)
        self.assertEqual([["2009-22", "111-22"], ["2007-11", "111-22"]], value)

        key, value = sxs.apply_layer("111-22-a")
        self.assertEqual("analyses", key)
        self.assertEqual([["2009-22", "111-22-a"]], value)

        self.assertEqual(None, sxs.apply_layer("222-22"))
