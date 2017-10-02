from unittest import TestCase
from regulations.generator import title_parsing


class RegTest(TestCase):
    def test_try_split(self):
        self.assertEqual(
            ['a', 'xb'],
            title_parsing.try_split('a:xb', ('|', ':', 'x')))

    def test_appendix_supplement_ap(self):
        elements = title_parsing.appendix_supplement({
            'index': ['204', 'A2'],
            'title': 'Appendix A2 to 204-First Appendix'})
        self.assertTrue(elements['is_appendix'])
        elements = title_parsing.appendix_supplement({
            'index': ['204', 'A'],
            'title': 'Appendix A to 204-First Appendix'})
        self.assertTrue(elements['is_appendix'])

    def test_section(self):
        elements = title_parsing.section({
            'index': ['204', '4'],
            'title': '204.4 Sauce'})

        self.assertTrue(elements['is_section'])
        self.assertEquals('Sauce', elements['sub_label'])

        elements = title_parsing.section({
            'index': ['204', '4'],
            'title': '204.4 [Reserved]'})

        self.assertTrue(elements['is_section'])
        self.assertEquals('[Reserved]', elements['sub_label'])

    def test_section_with_leading_symbol(self):
        elements = title_parsing.section({
            'index': ['204', '4'],
            'title': '\xc2\xa7 204.4 Foo bar',
        })
        self.assertEqual(elements['sub_label'], 'Foo bar')

    def test_section_with_leading_section(self):
        elements = title_parsing.section({
            'index': ['204', '4'],
            'title': '204.4 Foo bar',
        })
        self.assertEqual(elements['sub_label'], 'Foo bar')

    def test_section_without_leading_section(self):
        elements = title_parsing.section({
            'index': ['204', '4'],
            'title': 'Foo bar',
        })
        self.assertEqual(elements['sub_label'], 'Foo bar')

    def test_section_with_leading_symbol_but_without_leading_section(self):
        elements = title_parsing.section({
            'index': ['204', '4'],
            'title': '\xc2\xa7 Foo bar',
        })
        self.assertEqual(elements['sub_label'], 'Foo bar')
