from mock import Mock, patch
from django.conf import settings
from unittest import TestCase

from regulations.generator.layers.interpretations import InterpretationsLayer


class InterpretationsLayerTest(TestCase):
    def setUp(self):
        if not settings.configured:
            settings.configure(TEMPLATE_DEBUG=False, API_BASE='')

    @patch('regulations.generator.layers.interpretations.views'
           + '.partial.PartialInterpView')
    def test_apply_layer_extra_fields(self, piv):
        layer = {
            "200-2-b-3-i": [{
                'reference': '200-2-b-3-i-Interp',
                "text": "Some contents are here"
            }],
        }
        piv.as_view.return_value.return_value.content = 'content'

        il = InterpretationsLayer(layer)

        self.assertEqual(il.apply_layer('200-2-b-3-i'), ('interp', {
            'for_markup_id': '200-2-b-3-i',
            'label_id': '200-2-b-3-i-Interp',
            'label': '2(b)(3)(i)',
            'markup': 'content',
            'section_id': '200-Interp',
        }))

    @patch('regulations.generator.layers.interpretations.views'
           + '.partial.PartialInterpView')
    def test_apply_layer_section(self, piv):
        layer = {
            "200-2": [{
                "reference": "200-2-Interp",
                "text": "Some contents are here"
            }],
        }
        piv.as_view.return_value.return_value.content = 'content'
        il = InterpretationsLayer(layer)

        self.assertEqual('2', il.apply_layer('200-2')[1]['label'])

    @patch('regulations.generator.layers.interpretations.views'
           + '.partial.PartialInterpView')
    def test_apply_layer_appendix(self, piv):
        layer = {
            "200-Q-5": [{
                "reference": "200-Q-5-Interp",
                "text": "Some contents are here"
            }],
        }
        piv.as_view.return_value.return_value.content = 'content'
        il = InterpretationsLayer(layer)

        self.assertEqual('Appendix Q-5', il.apply_layer('200-Q-5')[1]['label'])

    @patch('regulations.generator.layers.interpretations.views'
           + '.partial.PartialInterpView')
    def test_apply_layer_section_different(self, piv):
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
        piv.as_view.return_value.return_value.content = 'content'
        il = InterpretationsLayer(layer)

        _, result = il.apply_layer('200-2-a')
        self.assertEqual('2(a)', result['label'])

        _, result = il.apply_layer('200-2-b')
        self.assertEqual('2(b)', result['label'])
