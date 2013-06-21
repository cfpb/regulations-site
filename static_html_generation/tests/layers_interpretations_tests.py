from layers.interpretations import InterpretationsLayer
from mock import Mock, patch
from unittest import TestCase

class InterpretationsLayerTest(TestCase):
    @patch('layers.interpretations.api_reader')
    def test_apply_layer_extra_fields(self, api_reader):
        layer = {
            "200-2-b-3-i": [{
                "reference": "200-Interpretations-2-(b)(3)(i)",
                "text": "Some contents are here"
            }],
        }
        api_reader.Client.return_value.regulation.return_value = {
            'some': 'node'
        }

        il = InterpretationsLayer(layer, 'test-version')
        il.builder = Mock()

        il.apply_layer('200-2-b-3-i')
        self.assertEqual(il.builder.tree, {
            'some': 'node',
            'interp_for_markup_id': '200-2-b-3-i',
            'interp_label': '2(b)(3)(i)'
        })

    @patch('layers.interpretations.api_reader')
    def test_apply_layer_section(self, api_reader):
        layer = {
            "200-2": [{
                "reference": "200-Interpretations-2",
                "text": "Some contents are here"
            }],
        }
        api_reader.Client.return_value.regulation.return_value = {
            'some': 'node'
        }

        il = InterpretationsLayer(layer, 'test-version')
        il.builder = Mock()

        il.apply_layer('200-2')
        self.assertEqual(il.builder.tree, {
            'some': 'node',
            'interp_for_markup_id': '200-2',
            'interp_label': '2'
        })

    @patch('layers.interpretations.api_reader')
    def test_apply_layer_appendix(self, api_reader):
        layer = {
            "200-Q-5": [{
                "reference": "200-Interpretations-Q-5",
                "text": "Some contents are here"
            }],
        }
        api_reader.Client.return_value.regulation.return_value = {
            'some': 'node'
        }

        il = InterpretationsLayer(layer, 'test-version')
        il.builder = Mock()

        il.apply_layer('200-Q-5')
        self.assertEqual(il.builder.tree, {
            'some': 'node',
            'interp_for_markup_id': '200-Q-5',
            'interp_label': 'Q-5'
        })
