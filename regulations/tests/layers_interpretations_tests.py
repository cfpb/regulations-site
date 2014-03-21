from mock import Mock, patch
from django.conf import settings
from unittest import TestCase

from regulations.generator.layers.interpretations import InterpretationsLayer


class InterpretationsLayerTest(TestCase):
    def setUp(self):
        if not settings.configured:
            settings.configure(TEMPLATE_DEBUG=False, API_BASE='')

    @patch('regulations.generator.layers.interpretations.generator')
    @patch('regulations.generator.layers.interpretations.SectionUrl')
    def test_apply_layer_extra_fields(self, su, generator):
        su.return_value.interp.return_value = '200-Subpart-Interp'
        layer = {
            "200-2-b-3-i": [{
                'reference': '200-2-b-3-i-Interp',
                "text": "Some contents are here"
            }],
        }
        il = InterpretationsLayer(layer)
        il.partial_view = Mock()
        il.partial_view.return_value.content = 'content'

        self.assertEqual(il.apply_layer('200-2-b-3-i'), ('interp', {
            'for_markup_id': '200-2-b-3-i',
            'for_label': '2(b)(3)(i)',
            'interps': [{
                'label_id': '200-2-b-3-i-Interp',
                'markup': 'content',
                'section_id': '200-Subpart-Interp'}]
        }))

    @patch('regulations.generator.layers.interpretations.generator')
    @patch('regulations.generator.layers.interpretations.SectionUrl')
    def test_apply_layer_section(self, su, generator):
        layer = {
            "200-2": [{
                "reference": "200-2-Interp",
                "text": "Some contents are here"
            }],
        }
        il = InterpretationsLayer(layer)
        il.partial_view = Mock()
        il.partial_view.return_value.content = 'content'

        self.assertEqual('2', il.apply_layer('200-2')[1]['for_label'])

    @patch('regulations.generator.layers.interpretations.generator')
    @patch('regulations.generator.layers.interpretations.SectionUrl')
    def test_apply_layer_multiple_matches(self, su, generator):
        layer = {
            "200-2": [{
                "reference": "200-2-Interp",
                "text": "Some contents are here"
            }, {
                "reference": "200-2_3-Interp",
                "text": "Some more contents are here"
            }],
        }
        il = InterpretationsLayer(layer)
        il.partial_view = Mock()
        il.partial_view.return_value.content = 'content'

        _, data = il.apply_layer('200-2')
        labels = [interp['label_id'] for interp in data['interps']]
        self.assertEqual(labels, ['200-2-Interp', '200-2_3-Interp'])

    @patch('regulations.generator.layers.interpretations.generator')
    @patch('regulations.generator.layers.interpretations.SectionUrl')
    def test_apply_layer_appendix(self, su, piv):
        layer = {
            "200-Q-5": [{
                "reference": "200-Q-5-Interp",
                "text": "Some contents are here"
            }],
        }
        il = InterpretationsLayer(layer)
        il.partial_view = Mock()
        il.partial_view.return_value.content = 'content'

        self.assertEqual('Appendix Q-5',
                         il.apply_layer('200-Q-5')[1]['for_label'])

    @patch('regulations.generator.layers.interpretations.generator')
    @patch('regulations.generator.layers.interpretations.SectionUrl')
    def test_apply_layer_section_different(self, su, generator):
        layer = {
            "200-2-a": [{
                "reference": "200-2-a-Interp",
                "text": "Some contents are here"
            }],
            "200-2-b": [{
                "reference": "200-2-a-Interp",
                "text": "Some contents are here"
            }],
        }
        il = InterpretationsLayer(layer)
        il.partial_view = Mock()
        il.partial_view.return_value.content = 'content'

        _, result = il.apply_layer('200-2-a')
        self.assertEqual('2(a)', result['for_label'])

        _, result = il.apply_layer('200-2-b')
        self.assertEqual('2(b)', result['for_label'])

    @patch('regulations.generator.layers.interpretations.generator')
    @patch('regulations.generator.layers.interpretations.SectionUrl')
    def test_apply_layer_cache(self, secturl, generator):
        il = InterpretationsLayer({
            '1234-56-a': [{'reference': '1234-56-a-Interp'}]}, version='vvvv')
        il.root_interp_label = '1234-56-Interp'
        il.partial_view = Mock()
        il.partial_view.return_value.content = 'content'
        il.apply_layer('1234-56')
        self.assertFalse(generator.generator.get_tree_paragraph.called)

        il.apply_layer('1234-56-a')
        self.assertTrue(generator.generator.get_tree_paragraph.called)
        args = generator.generator.get_tree_paragraph.call_args[0]
        # Note that this is grabbing the section's interps
        self.assertEqual('1234-56-Interp', args[0])
        self.assertEqual('vvvv', args[1])

    @patch('regulations.generator.layers.interpretations.views')
    def test_preprocess_root(self, views):
        node = {'text': 'tttt', 'children': [], 'node_type': 'regtext',
                'label': ['1234', '56', 'a']}
        il = InterpretationsLayer({})
        il.preprocess_root(node)
        self.assertEqual(il.root_interp_label, '1234-56-a-Interp')
