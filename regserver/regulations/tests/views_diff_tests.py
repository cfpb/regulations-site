from unittest import TestCase

from regulations.views.diff import *

class ChromeSectionDiffViewTests(TestCase):
    def test_diff_toc(self):
        """Integration test."""
        context = {
            'version': 'oldold',
            'main_content_context': {'newer_version': 'newnew'}
        }
        old_toc = [{'section_id': '8888-1', 'index': ['8888', '1']},
                   {'section_id': '8888-3', 'index': ['8888', '3']},
                   {'section_id': '8888-4', 'index': ['8888', '4']},
                   {'section_id': '8888-A', 'index': ['8888', 'A']},
                   {'section_id': '8888-B', 'index': ['8888', 'B']},
                   {'section_id': '8888-Interp', 'index': ['8888', 'Interp']}]
        diff = {
            '8888-2': {'op': 'added',
                       'node': {'title': '8888.2', 'label': ['8888', '2']}},
            '8888-C': {'op': 'added',
                       'node': {'title': 'App C', 'label': ['8888', 'C']}},
            '8888-1-a': {'op': 'modified'},
            '8888-B': {'op': 'deleted'},
            '8888-3-b': {'op': 'deleted'},
            '8888-B-1': {'op': 'modified'}
        }

        result = diff_toc(context, old_toc, diff)
        self.assertEqual(8, len(result))
        self.assertTrue('8888-1' in result[0]['url'])
        self.assertEqual('8888-1', result[0]['section_id'])
        self.assertEqual('modified', result[0]['op'])
        self.assertTrue('8888-2' in result[1]['url'])
        self.assertEqual('8888-2', result[1]['section_id'])
        self.assertEqual('added', result[1]['op'])
        self.assertTrue('8888-3' in result[2]['url'])
        self.assertEqual('8888-3', result[2]['section_id'])
        self.assertEqual('modified', result[2]['op'])
        self.assertTrue('8888-4' in result[3]['url'])
        self.assertEqual('8888-4', result[3]['section_id'])
        self.assertFalse('op' in result[3])
        self.assertTrue('8888-A' in result[4]['url'])
        self.assertEqual('8888-A', result[4]['section_id'])
        self.assertFalse('op' in result[4])
        self.assertTrue('8888-B' in result[5]['url'])
        self.assertEqual('8888-B', result[5]['section_id'])
        self.assertEqual('deleted', result[5]['op'])
        self.assertTrue('8888-C' in result[6]['url'])
        self.assertEqual('8888-C', result[6]['section_id'])
        self.assertEqual('added', result[6]['op'])
        self.assertTrue('8888-Interp' in result[7]['url'])
        self.assertEqual('8888-Interp', result[7]['section_id'])
        self.assertFalse('op' in result[7])
        for el in result:
            self.assertTrue('oldold', el['url'])
            self.assertTrue('newnew', el['url'])
