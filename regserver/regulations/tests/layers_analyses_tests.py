from regulations.generator.layers.analyses import *
from unittest import TestCase


class SectionBySectionLayerTest(TestCase):

    def test_apply_layer(self):
        layer = {
            "111-22": [{
                "reference": ["2007-22", "111-22"],
                "text": "Older analysis"
            }, {
                "reference": ["2009-11", "111-22"],
                "text": "Newer analysis"
            }],
            "111-22-a": [{
                "reference": ["2009-22", "111-22-a"],
                "text": "Paragraph analysis"
            }]
        }
        sxs = SectionBySectionLayer(layer)

        key, value = sxs.apply_layer("111-22")
        self.assertEqual("analyses", key)
        self.assertEqual([
            {'doc_number': '2009-11', 'label_id': '111-22', 'text': '111.22'},
            {'doc_number': '2009-22', 'label_id': '111-22-a',
             'text': '111.22(a)'}], value)

        key, value = sxs.apply_layer("111-22-a")
        self.assertEqual("analyses", key)
        self.assertEqual([{'doc_number': '2009-22', 'label_id': '111-22-a',
                           'text': '111.22(a)'}], value)

        self.assertEqual(None, sxs.apply_layer("222-22"))

    def test_to_template_dict(self):
        layer = {'555-22-Interp': [{'reference': ['aaa', '555-22-Interp']},
                                   {'reference': ['bbb', '555-22-Interp']},
                                   {'reference': ['ccc', '555-22-Interp']}]}
        sxs = SectionBySectionLayer(layer)

        self.assertEqual(sxs.to_template_dict('555-22-Interp'), [{
            'doc_number': 'ccc', 'label_id': '555-22-Interp',
            'text': 'Comment for 555.22'}])
