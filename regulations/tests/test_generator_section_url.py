from unittest import TestCase

from mock import patch

from regulations.generator.section_url import SectionUrl


class SectionUrlTest(TestCase):
    @patch('regulations.generator.section_url.fetch_toc')
    def test_interp(self, fetch_toc):
        fetch_toc.return_value = [
            {'index': ['200', '1'], 'is_section': True},
            {'index': ['200', '2'], 'is_section': True},
            {'index': ['200', 'A'], 'is_appendix': True}]
        self.assertEqual('200-Subpart-Interp',
                         SectionUrl().interp(['200', '1', 'Interp'], 'vvvv'))
        self.assertEqual('200-Subpart-Interp',
                         SectionUrl().interp(['200', '2', 'Interp'], 'vvvv'))
        self.assertEqual('200-Appendices-Interp',
                         SectionUrl().interp(['200', 'A', 'Interp'], 'vvvv'))

        fetch_toc.return_value = [
            {'index': ['200', 'Subpart', 'A'], 'is_subpart': True,
             'sub_toc': [{'index': ['200', '1'], 'is_section': True},
                         {'index': ['200', '2'], 'is_section': True}]},
            {'index': ['200', 'A'], 'is_appendix': True},
            {'index': ['200', 'Interp'], 'is_supplement': True,
             'sub_toc': [{'index': ['200', 'Interp', 'h1'],
                          'section_id': '200-Interp-h1'},
                         {'index': ['200', 'Subpart', 'A', 'Interp'],
                          'is_subterp': True},
                         {'index': ['200', 'Appendices', 'Interp'],
                          'is_subterp': True}]}]
        self.assertEqual('200-Subpart-A-Interp',
                         SectionUrl().interp(['200', '1', 'Interp'], 'vvvv'))
        self.assertEqual('200-Subpart-A-Interp',
                         SectionUrl().interp(['200', '2', 'Interp'], 'vvvv'))
        self.assertEqual('200-Appendices-Interp',
                         SectionUrl().interp(['200', 'A', 'Interp'], 'vvvv'))
        self.assertEqual('200-Interp-h1',
                         SectionUrl().interp(['200', 'Interp', 'h1', 'p1'],
                         'vvvv'))
        self.assertEqual('200-Interp-h1',
                         SectionUrl().interp(['200', 'Interp', 'h1'], 'vvvv'))
        self.assertTrue('200-Subpart-A',
                        SectionUrl().interp(['200', '2', 'e', 'Interp', '1'],
                                            'verver'))

    def test_of(self):
        url = SectionUrl.of(['303', '1'], 'vvv', False)
        self.assertEquals('#303-1', url)

        url = SectionUrl.of(['303', '1', 'b'], 'vvv', False)
        self.assertEquals('#303-1-b', url)

        url = SectionUrl.of(['303'], 'vvv', False)
        self.assertEquals('#303', url)

        url = SectionUrl.of(['303', '1', 'b'], 'vvv', True)
        self.assertEquals('/303-1/vvv#303-1-b', url)

        self.assertTrue('999-88/verver#999-88-e' in
                        SectionUrl.of(['999', '88', 'e'], 'verver', True))
        self.assertEqual(
            '#999-88-e', SectionUrl.of(['999', '88', 'e'], 'verver', False))

        self.assertEqual(
            '#999-Subpart-Interp',
            SectionUrl.of(['999', 'Subpart', 'Interp'], 'verver', False))
        self.assertEqual(
            '#999-Subpart-A-Interp',
            SectionUrl.of(['999', 'Subpart', 'A', 'Interp'], 'verver', False))
        self.assertEqual(
            '#999-Appendices-Interp',
            SectionUrl.of(['999', 'Appendices', 'Interp'], 'verver', False))
