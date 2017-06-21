#vim: set encoding=utf-8
from unittest import TestCase
from mock import patch
from regulations.views import navigation


class NavigationTest(TestCase):
    def test_get_labels(self):
        label = '204-1-a'
        self.assertEquals(
            ['204', '1', 'a'], navigation.get_labels(label))

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

    @patch('regulations.views.navigation.fetch_toc')
    def test_nav_sections(self, fetch_toc):
        fetch_toc.return_value = [
            {'index': ['204', '1'], 'title': '§ 204.1 First'},
            {'index': ['204', '3'], 'title': '§ 204.3 Third'}]
        nav = navigation.nav_sections('204-1', 'ver')
        p, n = nav
        self.assertEquals(None, p)
        self.assertEquals(['204', '3'], n['index'])
        self.assertEquals('§ 204.3 Third', n['title'])

    @patch('regulations.views.navigation.fetch_toc')
    @patch('regulations.views.navigation.SectionUrl')
    def test_nav_sections_prefix(self, su, fetch_toc):
        fetch_toc.return_value = [
            {'index': ['204', '1'], 'title': '§ 204.1 First',
             'is_section': True},
            {'index': ['204', 'A'], 'title': 'Appendix A'},
            {'index': ['204', 'Subpart', 'Interp'],
             'title': 'Regulation Text', 'is_subterp': True}]
        nav = navigation.nav_sections('204-A', 'ver')
        p, n = nav
        self.assertEqual(['204', '1'], p['index'])
        self.assertEqual('&sect;&nbsp;', p['markup_prefix'])
        self.assertEqual(['204', 'Subpart', 'Interp'], n['index'])
        self.assertEqual('Interpretations For ', n['markup_prefix'])

    @patch('regulations.views.navigation.fetch_toc')
    def test_nav_sections_appendix(self, fetch_toc):
        fetch_toc.return_value = [
            {'index': ['204', '1'], 'title': u'§ 204.1 First'},
            {'index': ['204', 'A'],
             'title': 'Appendix A to Part 204 - Model Forms'}]
        nav = navigation.nav_sections('204-1', 'ver')
        p, n = nav
        self.assertEquals(None, p)
        self.assertEquals(['204', 'A'], n['index'])
        self.assertEquals('Appendix A to Part 204 - Model Forms',
                          n['title'])

    @patch('regulations.views.navigation.fetch_toc')
    def test_nav_sections_subparts(self, fetch_toc):
        fetch_toc.return_value = [
            {'index': ['204', '1'], 'title': u'§ 204.1 First'},
            {'index': ['204', '2'], 'title': u'§ 204.2 Second'},
            {'index': ['204', '3'], 'title': u'§ 204.3 Third'},
            {'index': ['204', 'A'], 'title': 'Appendix A'},
            {'index': ['204', 'Subpart', 'A', 'Interp'], 'title': 'Subpart A'},
            {'index': ['204', 'Appendices', 'Interp'],
             'title': 'Appendices'}]
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
        self.assertEquals(['204', 'Subpart', 'A', 'Interp'], n['index'])

        nav = navigation.nav_sections('204-Subpart-A-Interp', 'ver')
        p, n = nav
        self.assertEquals(['204', 'A'], p['index'])
        self.assertEquals(['204', 'Appendices', 'Interp'], n['index'])

        nav = navigation.nav_sections('204-Appendices-Interp', 'ver')
        p, n = nav
        self.assertEquals(['204', 'Subpart', 'A', 'Interp'], p['index'])
        self.assertEquals(None, n)
