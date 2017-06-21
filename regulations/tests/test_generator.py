from unittest import TestCase

from mock import patch

from regulations.generator import generator
from regulations.generator.layers.layers_applier import InlineLayersApplier
from regulations.generator.layers.layers_applier import ParagraphLayersApplier
from regulations.generator.layers.layers_applier\
    import SearchReplaceLayersApplier


class GeneratorTest(TestCase):

    @patch('regulations.generator.generator.api_reader')
    def test_get_regulation_extra_fields(self, api_reader):
        reg = {
            'text': '', 'children': [], 'label': ['8675'],
            'title': 'Contains no part info'
        }
        api_reader.ApiReader.return_value.regulation.return_value = reg

        r = generator.get_regulation('8675', 'ver')
        self.assertFalse('title_clean' in r)
        self.assertFalse('reg_letter' in r)

        reg['title'] = 'part 8675 - Some title'
        r = generator.get_regulation('8675', 'ver')
        self.assertTrue('title_clean' in r)
        self.assertEqual('Some title', r['title_clean'])
        self.assertFalse('reg_letter' in r)

        del reg['title_clean']
        reg['title'] = 'part 8675 - Some title (RegUlation RR)'
        r = generator.get_regulation('8675', 'ver')
        self.assertTrue('title_clean' in r)
        self.assertEqual('Some title', r['title_clean'])
        self.assertTrue('reg_letter' in r)
        self.assertEqual('RR', r['reg_letter'])

    @patch('regulations.generator.generator.api_reader')
    def test_get_tree_paragraph(self, api_reader):
        node = {'some': 'text'}
        api_reader.ApiReader.return_value.regulation.return_value = node

        p = generator.get_tree_paragraph('some-id', 'some-version')
        self.assertEqual(node, p)
        self.assertEqual(
            ('some-id', 'some-version'),
            api_reader.ApiReader.return_value.regulation.call_args[0])

    @patch('regulations.generator.generator.api_reader')
    def test_get_diff_json(self, api_reader):
        diff = {'some': 'diff'}
        api_reader.ApiReader.return_value.diff.return_value = diff
        d = generator.get_diff_json('204', 'old', 'new')
        self.assertEqual(diff, d)
        self.assertEqual(
            ('204', 'old', 'new'),
            api_reader.ApiReader.return_value.diff.call_args[0])

    @patch('regulations.generator.generator.api_reader')
    def test_get_notice(self, api_reader):
        notice = {'some': 'notice'}
        api_reader.ApiReader.return_value.notice.return_value = notice
        n = generator.get_notice('111', '204-1234')
        self.assertEqual(notice, n)
        self.assertEqual(
            ('111', '204-1234',),
            api_reader.ApiReader.return_value.notice.call_args[0])

    @patch('regulations.generator.generator.get_diff_json')
    def test_get_diff_applier(self, get_diff_json):
        diff = {'some': 'diff'}
        get_diff_json.return_value = diff
        da = generator.get_diff_applier('204', 'old', 'new')
        self.assertEqual(da.diff, diff)
        self.assertEqual(
            ('204', 'old', 'new'),
            get_diff_json.call_args[0])

    def test_layercreator_layers(self):
        """ A LAYER entry must have three pieces of information specified. """

        for l, v in generator.LayerCreator.LAYERS.items():
            self.assertEqual(len(v), 3)

    def test_layercreator_getappliers(self):
        creator = generator.LayerCreator()
        appliers = creator.get_appliers()
        self.assertEquals(len(appliers), 3)

        i_applier, p_applier, s_applier = appliers

        self.assertTrue(isinstance(i_applier, InlineLayersApplier))
        self.assertTrue(isinstance(p_applier, ParagraphLayersApplier))
        self.assertTrue(isinstance(s_applier, SearchReplaceLayersApplier))

    @patch('regulations.generator.generator.LayerCreator.get_layer_json')
    def test_add_layer(self, get_layer_json):
        get_layer_json.return_value = {'layer': 'layer'}
        creator = generator.LayerCreator()
        creator.add_layer('meta', '205', 'verver')
        i, p, s = creator.get_appliers()
        self.assertEquals(len(p.layers), 1)

        get_layer_json.return_value = None
        creator = generator.LayerCreator()
        creator.add_layer('meta', '205', 'verver')
        i, p, s = creator.get_appliers()
        self.assertEquals(len(p.layers), 0)

    @patch('regulations.generator.generator.LayerCreator.get_layer_json')
    def test_add_layers(self, get_layer_json):
        get_layer_json.return_value = {'layer': 'layer'}

        creator = generator.LayerCreator()
        creator.add_layers(
            ['meta', 'graphics', 'internal'], '205', 'verver',
            sectional=True)
        i, p, s = creator.get_appliers()
        self.assertEquals(len(p.layers), 1)
        self.assertEquals(len(i.layers), 1)
        self.assertEquals(len(s.layers), 1)

        internal_citation_layer = i.layers['internal']
        self.assertTrue(internal_citation_layer.sectional)
        self.assertEquals(internal_citation_layer.version, 'verver')
