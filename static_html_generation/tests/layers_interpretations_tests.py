from layers.interpretations import InterpretationsLayer
from unittest import TestCase

class InterpretationsLayerTest(TestCase):
    def test_apply_layer(self):
        layer = {
                "200-2-b": [{
                    "reference": "200-Interpretations-2-b",
                    "text": "Some contents are here"
                    }],
                "200-2-b-ii": [{
                    "reference": "200-Interpretations-2-b-ii",
                    "text": "Inner interpretaton"
                    }, {
                    "reference": "200-Interpretations-2-b",
                    "text": "Some contents are here"
                    }]}
        il = InterpretationsLayer(layer)

        key, value = il.apply_layer("200-2-b")
        self.assertEqual('200-Interpretations-2-b', value)
        self.assertEqual('interpretations', key)

        key, value = il.apply_layer("200-2-b-ii")
        self.assertEqual('200-Interpretations-2-b-ii', value)
        self.assertEqual('interpretations', key)

        self.assertEqual(None, il.apply_layer("200-2-b-iii"))
