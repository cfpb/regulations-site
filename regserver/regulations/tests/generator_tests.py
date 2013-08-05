from unittest import TestCase

from mock import patch

from regulations.generator import generator
from regulations.generator.layers.layers_applier import InlineLayersApplier
from regulations.generator.layers.layers_applier import ParagraphLayersApplier
from regulations.generator.layers.layers_applier import SearchReplaceLayersApplier


class GeneratorTest(TestCase):
    def test_create_sectional_citation_layer(self):
        icl = generator.create_sectional_citation_layer(None, '1023')
        self.assertTrue(icl.generate_sectional)
        self.assertEquals(icl.reg_version, '1023')

    def test_get_single_section(self):
        full_regulation = {'children':[{'label':{'text': '12-2'}}, 
                                {'label':{'text':'13-1'}}]}
        single = generator.get_single_section(full_regulation, '13-1')
        self.assertEquals({'label':{'text':'13-1'}}, single)

    def test_single_section_none(self):
        full_regulation = {'children':[{'label':{'text': '12-2'}}, 
                                {'label':{'text':'13-1'}}]}
        single = generator.get_single_section(full_regulation, '14-1')
        self.assertEquals(None, single)

    @patch('regulations.generator.generator.api_reader')
    def test_get_regulation_extra_fields(self, api_reader):
        reg = {'text': '', 'children': [], 'label': {
            'text': '8675', 
            'parts': ['8675'],
            'title': 'Contains no part info'
        }}
        api_reader.Client.return_value.regulation.return_value = reg

        r = generator.get_regulation('8675', 'ver')
        self.assertFalse('title_clean' in r['label'])
        self.assertFalse('reg_letter' in r['label'])

        reg['label']['title'] = 'part 8675 - Some title'
        r = generator.get_regulation('8675', 'ver')
        self.assertTrue('title_clean' in r['label'])
        self.assertEqual('Some title', r['label']['title_clean'])
        self.assertFalse('reg_letter' in r['label'])

        del reg['label']['title_clean']
        reg['label']['title'] = 'part 8675 - Some title (RegUlation RR)'
        r = generator.get_regulation('8675', 'ver')
        self.assertTrue('title_clean' in r['label'])
        self.assertEqual('Some title', r['label']['title_clean'])
        self.assertTrue('reg_letter' in r['label'])
        self.assertEqual('RR', r['label']['reg_letter'])

    @patch('regulations.generator.generator.api_reader')
    def test_get_tree_paragraph(self, api_reader):
        node = {'some': 'text'}
        api_reader.Client.return_value.regulation.return_value = node

        p = generator.get_tree_paragraph('some-id', 'some-version')
        self.assertEqual(node, p)
        self.assertEqual(('some-id', 'some-version'),
                api_reader.Client.return_value.regulation.call_args[0])

    def test_layercreator_layers(self):
        """ A LAYER entry must have three pieces of information specified. """

        for l,v in generator.LayerCreator.LAYERS.items():
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
        creator = generator.LayerCreator()
        get_layer_json.return_value = {'layer':'layer'}
        creator.add_layer('meta', '205', 'verver')
        i,p,s = creator.get_appliers()
        self.assertEquals(len(p.layers), 1)

    @patch('regulations.generator.generator.LayerCreator.get_layer_json')
    def test_add_layers(self, get_layer_json):
        get_layer_json.return_value = {'layer':'layer'}

        creator = generator.LayerCreator()
        creator.add_layers(['meta', 'graphics', 'internal'], '205', 'verver',
                sectional=True)
        i,p,s =  creator.get_appliers()
        self.assertEquals(len(p.layers), 1)
        self.assertEquals(len(i.layers), 1)
        self.assertEquals(len(s.layers), 1)

        internal_citation_layer = i.layers[0]
        self.assertTrue(internal_citation_layer.generate_sectional)
        self.assertEquals(internal_citation_layer.reg_version, 'verver')

    @patch('regulations.generator.generator.LayerCreator.get_layer_json')
    def test_get_creator_all_section_layers(self, get_layer_json):
        get_layer_json.return_value = {'layer':'layer'}
        creator = generator.get_creator_all_section_layers('205', 'verver')

        self.assertEquals(len(creator.appliers['inline'].layers), 2)
        self.assertEquals(len(creator.appliers['search_replace'].layers), 3)
        self.assertEquals(len(creator.appliers['paragraph'].layers), 3)

        
