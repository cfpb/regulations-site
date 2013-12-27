from unittest import TestCase

from mock import patch

from regulations.generator.layers.formatting import TableLayer


class TableLayerTest(TestCase):
    @patch('regulations.generator.layers.formatting.loader')
    def test_apply_layer(self, loader):
        tl = TableLayer()
        render = loader.get_template.return_value.render

        tl.apply_layer('Contains\nNo\nTables', '111-22')
        self.assertFalse(render.called)

        table = '|Header1|Header2|Header3|\n'
        table += '|---|---|---|\n'
        table += '|Cell1-1|Cell1-2|Cell1-3|\n'
        table += '|Cell2-1|Cell2-2|Cell2-3|\n'
        table += '|Cell3-1|Cell3-2|Cell3-3|'
        tl.apply_layer(table, '111-22')
        self.assertTrue(render.called)

        context = render.call_args[0][0]
        self.assertEqual(['Header1', 'Header2', 'Header3'], context['header'])
        self.assertEqual(3, len(context['rows']))
        r1, r2, r3 = context['rows']
        self.assertEqual(['Cell1-1', 'Cell1-2', 'Cell1-3'], r1)
        self.assertEqual(['Cell2-1', 'Cell2-2', 'Cell2-3'], r2)
        self.assertEqual(['Cell3-1', 'Cell3-2', 'Cell3-3'], r3)
