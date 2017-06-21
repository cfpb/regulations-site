from unittest import TestCase

from mock import patch

from regulations.generator import subterp


class SubterpTest(TestCase):
    @patch('regulations.generator.subterp.fetch_toc')
    def test_filter_by_subterp(self, fetch_toc):
        nodes = [{'label': ['1005', 'h1', 'Interp']},
                 {'label': ['1005', '2', 'Interp']},
                 {'label': ['1005', '3', 'Interp']},
                 {'label': ['1005', '4', 'Interp']},
                 {'label': ['1005', 'A', 'Interp']},
                 {'label': ['1005', 'A_B', 'Interp']},
                 {'label': ['1005', 'B', 'Interp']}]
        self.assertEqual(nodes[1:4], subterp.filter_by_subterp(
            nodes, ['1005', 'Subpart', 'Interp'], 'vvvv'))
        self.assertFalse(fetch_toc.called)

        self.assertEqual(nodes[4:], subterp.filter_by_subterp(
            nodes, ['1005', 'Appendices', 'Interp'], 'vvvv'))
        self.assertFalse(fetch_toc.called)

        fetch_toc.return_value = [
            {'index': ['1005', 'Subpart', 'A'],
             'sub_toc': [{'index': ['1005', '1']}, {'index': ['1005', '2']}]},
            {'index': ['1005', 'Subpart', 'B'],
             'sub_toc': [{'index': ['1005', '3']}, {'index': ['1005', '4']}]},
            {'index': ['1005', 'A']},
            {'index': ['1005', 'B']},
            {'index': ['1005', 'Interp'],
             'sub_toc': [{'index': ['1005', 'Subpart', 'A', 'Interp']},
                         {'index': ['1005', 'Subpart', 'B', 'Interp']},
                         {'index': ['1005', 'Appendices', 'Interp']}]}]
        self.assertEqual(nodes[1:2], subterp.filter_by_subterp(
            nodes, ['1005', 'Subpart', 'A', 'Interp'], 'vvvv'))
        self.assertEqual(nodes[2:4], subterp.filter_by_subterp(
            nodes, ['1005', 'Subpart', 'B', 'Interp'], 'vvvv'))
