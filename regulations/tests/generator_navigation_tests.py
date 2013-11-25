#vim: set encoding=utf-8
from unittest import TestCase
from mock import patch
from regulations.generator import navigation


class NavigationTest(TestCase):

    def test_get_labels(self):
        label = '204-1-a'
        self.assertEquals(
            ['204', '1', 'a'], navigation.get_labels(label))

    def test_up_level(self):
        label = ['204', '1', 'a']
        self.assertEquals('204-1', navigation.up_level(label))

    def test_is_last(self):
        l = [1, 2, 3]
        self.assertFalse(navigation.is_last(1, l))
        self.assertTrue(navigation.is_last(2, l))

    def test_choose_next_section(self):
        l = [1, 2, 3]
        self.assertEquals(3, navigation.choose_next_section(1, l))
        self.assertEquals(None, navigation.choose_next_section(2, l))

    def test_choose_previous_section(self):
        l = [1,  2, 3]
        self.assertEquals(1, navigation.choose_previous_section(1, l))
        self.assertEquals(2, navigation.choose_previous_section(2, l))
        self.assertEquals(None, navigation.choose_previous_section(0, l))

    @patch('regulations.generator.navigation.get_toc')
    def test_nav_sections(self, get_toc):
        get_toc.return_value = {
            '204': [
                {'index': ['204', '1'], 'title': '§ 204.1 First'},
                {'index': ['204', '3'], 'title': '§ 204.3 Third'}]}
        nav = navigation.nav_sections('204-1', 'ver')
        p, n = nav
        self.assertEquals(None, p)
        self.assertEquals({'index': ['204', '3'], 'title': '§ 204.3 Third'}, n)

    @patch('regulations.generator.navigation.get_toc')
    def test_nav_sections_appendix(self, get_toc):
        get_toc.return_value = {
            '204': [
                {'index': ['204', '1'], 'title': u'§ 204.1 First'},
                {
                    'index': ['204', 'A'],
                    'title': 'Appendix A to Part 204 - Model Forms'}]}
        nav = navigation.nav_sections('204-1', 'ver')
        p, n = nav
        self.assertEquals(None, p)
        self.assertEquals({
            'index': ['204', 'A'],
            'title': 'Appendix A to Part 204 - Model Forms'}, n)

        e = navigation.parse_section_title(n)
        self.assertEquals('204-A', e['section_id'])
        self.assertEquals('Appendix A to Part 204', e['label'])
        self.assertEquals('Model Forms', e['sub_label'])

    @patch('regulations.generator.navigation.get_toc')
    def test_nav_sections_subparts(self, get_toc):
        get_toc.return_value = {
            '204': [
                {'index': ['204', 'Subpart', 'A'], 'title': 'Subpart A'},
                {'index': ['204', 'A'], 'title': 'Appendix A'},
                {'index': ['204', 'Interp'], 'title': 'Interpretations'}],
            '204-Subpart-A': [
                {'index': ['204', '1'], 'title': u'§ 204.1 First'},
                {'index': ['204', '2'], 'title': u'§ 204.2 Second'},
                {'index': ['204', '3'], 'title': u'§ 204.3 Third'}]}
        nav = navigation.nav_sections('204-1', 'ver')
        p, n = nav
        self.assertEquals(None, p)
        self.assertEquals(['204', '2'], n['index'])

        nav = navigation.nav_sections('204-3', 'ver')
        p, n = nav
        self.assertEquals(['204', '2'], p['index'])
        self.assertEquals(['204', 'A'], n['index'])

        nav = navigation.nav_sections('204-A', 'ver')
        p, n = nav
        self.assertEquals(['204', '3'], p['index'])
        self.assertEquals(['204', 'Interp'], n['index'])

        nav = navigation.nav_sections('204-Interp', 'ver')
        p, n = nav
        self.assertEquals(['204', 'A'], p['index'])
        self.assertEquals(None, n)
