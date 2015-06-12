from unittest import TestCase

from mock import Mock, patch

from regulations.generator.layers.formatting import FormattingLayer


class FormattingLayerTest(TestCase):
    @patch('regulations.generator.layers.formatting.loader')
    def test_apply_layer(self, loader):
        render = loader.get_template.return_value.render

        table_data = {'header': [[{'colspan': 2, 'rowspan': 1,
                                   'text': 'Title'}]],
                      'rows': [['cell 11', 'cell 12'], ['cell 21', 'cell 22']]}
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
        self.assertEqual(context['header'],
                         [[{'colspan': 2, 'rowspan': 1, 'text': 'Title'}]])

    @patch('regulations.generator.layers.formatting.loader')
    def test_apply_layer_note(self, loader):
        note_mock = Mock()
        loader.get_template.side_effect = lambda arg: note_mock if "note" in arg else Mock()
        render = note_mock.render

        fence_data = {'type': 'note',
                      'lines': ['Note:', '1. Content1', '2. Content2']}
        data = {'111-1': [],
                '111-2': [{}],
                '111-3': [{'text': 'original', 'locations': [0],
                           'fence_data': fence_data}]}
        fl = FormattingLayer(data)
        self.assertEqual([], fl.apply_layer('111-0'))
        self.assertEqual([], fl.apply_layer('111-1'))
        self.assertEqual([], fl.apply_layer('111-2'))
        self.assertFalse(render.called)

        result = fl.apply_layer('111-3')
        self.assertEqual(len(result), 1)
        self.assertEqual('original', result[0][0])
        self.assertEqual([0], result[0][2])
        self.assertTrue(render.called)
        context = render.call_args[0][0]
        self.assertEqual(context['lines'],
                         ['1. Content1', '2. Content2'])

    @patch('regulations.generator.layers.formatting.loader')
    def test_apply_layer_code(self, loader):
        code_mock = Mock()
        loader.get_template.side_effect = lambda arg: code_mock if "code" in arg else Mock()
        render = code_mock.render

        fence_data = {'type': 'python',
                      'lines': ['def double(x):', '    return x + x']}
        data = {'111-1': [],
                '111-2': [{}],
                '111-3': [{'text': 'original', 'locations': [0],
                           'fence_data': fence_data}]}
        fl = FormattingLayer(data)
        self.assertEqual([], fl.apply_layer('111-0'))
        self.assertEqual([], fl.apply_layer('111-1'))
        self.assertEqual([], fl.apply_layer('111-2'))
        self.assertFalse(render.called)

        result = fl.apply_layer('111-3')
        self.assertEqual(len(result), 1)
        self.assertEqual('original', result[0][0])
        self.assertEqual([0], result[0][2])
        self.assertTrue(render.called)
        context = render.call_args[0][0]
        self.assertEqual(context['lines'],
                         ['def double(x):', '    return x + x'])

    @patch('regulations.generator.layers.formatting.loader')
    def test_apply_layer_subscript(self, loader):
        subscript_mock = Mock()
        loader.get_template.side_effect = lambda arg: subscript_mock if "subscript" in arg else Mock()
        render = subscript_mock.render

        subscript_data = {'variable': 'abc', 'subscript': '123'}
        data = {'111-1': [],
                '111-2': [{}],
                '111-3': [{'text': 'abc_{123}', 'locations': [0, 1, 2],
                           'subscript_data': subscript_data}]}
        fl = FormattingLayer(data)
        self.assertEqual([], fl.apply_layer('111-0'))
        self.assertEqual([], fl.apply_layer('111-1'))
        self.assertEqual([], fl.apply_layer('111-2'))
        self.assertFalse(render.called)

        result = fl.apply_layer('111-3')
        self.assertEqual(len(result), 1)
        self.assertEqual('abc_{123}', result[0][0])
        self.assertEqual([0, 1, 2], result[0][2])
        self.assertTrue(render.called)
        context = render.call_args[0][0]
        self.assertEqual(context['variable'], 'abc')
        self.assertEqual(context['subscript'], '123')


    @patch('regulations.generator.layers.formatting.loader')
    def test_apply_layer_dash(self, loader):
        dash_mock = Mock()
        loader.get_template.side_effect = lambda arg: dash_mock if "dash" in arg else Mock()
        render = dash_mock.render

        dash_data = {'text': 'This is an fp-dash'}
        data = {'111-1': [],
                '111-2': [{}],
                '111-3': [{'text': 'This is an fp-dash_____', 'locations': [0],
                           'dash_data': dash_data}]}
        fl = FormattingLayer(data)
        self.assertEqual([], fl.apply_layer('111-0'))
        self.assertEqual([], fl.apply_layer('111-1'))
        self.assertEqual([], fl.apply_layer('111-2'))
        self.assertFalse(render.called)

        result = fl.apply_layer('111-3')
        self.assertEqual(len(result), 1)
        self.assertEqual('This is an fp-dash_____', result[0][0])
        self.assertEqual([0], result[0][2])
        self.assertTrue(render.called)
        context = render.call_args[0][0]
        self.assertEqual(context['text'], 'This is an fp-dash')
