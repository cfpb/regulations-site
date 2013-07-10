from unittest import TestCase

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

