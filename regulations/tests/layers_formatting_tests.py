from unittest import TestCase

from mock import patch

from regulations.generator.layers.formatting import FormattingLayer


class FormattingLayerTest(TestCase):
    @patch('regulations.generator.layers.formatting.loader')
    def test_apply_layer(self, loader):
        render = loader.get_template.return_value.render

        table_data = {"table": "data"}
        data = {'111-1': [],
                '111-2': [{}], 
                '111-3': [{'text': 'original', 'locations': [0, 2],
                                   'table_data': table_data}]}
        fl = FormattingLayer(data)
        self.assertEqual([], fl.apply_layer('111-0'))
        self.assertEqual([], fl.apply_layer('111-1'))
        self.assertEqual([], fl.apply_layer('111-2'))
        self.assertFalse(render.called)

        result = fl.apply_layer('111-3')
        self.assertEqual(len(result), 1)
        self.assertEqual('original', result[0][0])
        self.assertEqual([0, 2], result[0][2])
        self.assertTrue(render.called)
        context = render.call_args[0][0]
        self.assertEqual(context['table'], 'data')
