from layers.interpretations import InterpretationsLayer
from mock import Mock, patch
from unittest import TestCase

class InterpretationsLayerTest(TestCase):
    @patch('layers.interpretations.loader.get_template')
    def test_apply_layer(self, get_template):
        #get_template.return_value = Mock()
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

        il.apply_layer("some text", "200-2-b")
        context = get_template.return_value.render.call_args[0][0]
        self.assertTrue('interpretation_ref' in context)
        self.assertEqual('200-Interpretations-2-b',
            context['interpretation_ref'])
        self.assertTrue('paragraph_text' in context)
        self.assertEqual('some text', context['paragraph_text'])

        get_template.reset_mock()
        il.apply_layer("another", "200-2-b-ii")
        context = get_template.return_value.render.call_args[0][0]
        self.assertTrue('interpretation_ref' in context)
        self.assertEqual('200-Interpretations-2-b-ii',
            context['interpretation_ref'])
        self.assertTrue('paragraph_text' in context)
        self.assertEqual('another', context['paragraph_text'])

        get_template.reset_mock()
        il.apply_layer("another", "200-2-b-iii")
        self.assertFalse(get_template.called)
