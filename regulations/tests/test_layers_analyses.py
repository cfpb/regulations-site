#vim: set encoding=utf-8
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
            {'doc_number': '2009-11', 'label_id': '111-22', 'text': u'§ 22'},
            {'doc_number': '2009-22', 'label_id': '111-22-a',
             'text': u'§ 22(a)'}], value)

        key, value = sxs.apply_layer("111-22-a")
        self.assertEqual("analyses", key)
        self.assertEqual([{'doc_number': '2009-22', 'label_id': '111-22-a',
                           'text': u'§ 22(a)'}], value)

        self.assertEqual(None, sxs.apply_layer("222-22"))

    def test_apply_layer_interps(self):
        layer = {
            '111-22': [{'reference': ['2007-22', '111-22']}],
            '111-22-Interp': [{'reference': ['2007-22', '111-22-Interp']}],
            '111-22-Interp-2': [{'reference': ['2007-22', '111-22-Interp-2']}]
        }
        sxs = SectionBySectionLayer(layer)

        _, value = sxs.apply_layer('111-22')
        self.assertEqual(
            [{'doc_number': '2007-22', 'label_id': '111-22', 'text': u'§ 22'}],
            value)
        _, value = sxs.apply_layer('111-22-Interp')
        self.assertEqual([
            {'doc_number': '2007-22', 'label_id': '111-22-Interp',
             'text': 'Comment for 111.22'},
            {'doc_number': '2007-22', 'label_id': '111-22-Interp-2',
             'text': 'Comment for 111.22-2'}], value)
        _, value = sxs.apply_layer('111-22-Interp')
        self.assertEqual([
            {'doc_number': '2007-22', 'label_id': '111-22-Interp',
             'text': 'Comment for 111.22'},
            {'doc_number': '2007-22', 'label_id': '111-22-Interp-2',
             'text': 'Comment for 111.22-2'}], value)
        _, value = sxs.apply_layer('111-22-Interp-2')
        self.assertEqual([
            {'doc_number': '2007-22', 'label_id': '111-22-Interp-2',
             'text': 'Comment for 111.22-2'}], value)

    def test_to_template_dict(self):
        layer = {'555-22-Interp': [{'reference': ['aaa', '555-22-Interp']},
                                   {'reference': ['bbb', '555-22-Interp']},
                                   {'reference': ['ccc', '555-22-Interp']}]}
        sxs = SectionBySectionLayer(layer)

        self.assertEqual(sxs.to_template_dict('555-22-Interp'), [{
            'doc_number': 'ccc', 'label_id': '555-22-Interp',
            'text': 'Comment for 555.22'}])

    def test_sort_analyses(self):
        """ Here we ensure that roman numerals are sorted correctly. """
        analyses = [
            {'label_id': '200-20-d-2-viii'},
            {'label_id': '200-20-d-2-ix'},
            {'label_id': '200-20-d-2-iv'},
            {'label_id': '200-20-d-2-v'},
            {'label_id': '200-20-d-2-vi'},
            {'label_id': '200-20-d-2-x'},
            {'label_id': '200-20-d-2-xi'},
        ]

        sorted_analyses = sort_analyses(analyses)
        labels = [a['label_id'] for a in sorted_analyses]
        self.assertEqual([
            '200-20-d-2-iv',
            '200-20-d-2-v',
            '200-20-d-2-vi',
            '200-20-d-2-viii',
            '200-20-d-2-ix',
            '200-20-d-2-x',
            '200-20-d-2-xi'], labels)
