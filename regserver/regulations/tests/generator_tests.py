from unittest import TestCase

from mock import patch

from regulations.generator import generator


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
