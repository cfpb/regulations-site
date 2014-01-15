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
            {'index': ['200', 'A'], 'is_appendix': True}]
        self.assertEqual('200-Subpart-A-Interp',
                         SectionUrl().interp(['200', '1', 'Interp'], 'vvvv'))
        self.assertEqual('200-Subpart-A-Interp',
                         SectionUrl().interp(['200', '2', 'Interp'], 'vvvv'))
        self.assertEqual('200-Appendices-Interp',
                         SectionUrl().interp(['200', 'A', 'Interp'], 'vvvv'))
