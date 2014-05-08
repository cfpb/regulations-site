#vim: set fileencoding=utf-8
from unittest import TestCase

from mock import patch

from regulations.generator import toc


class TocTest(TestCase):
    def test_toc_sect_appendix(self):
        data = {'title': u'§ 1026.1 - Authority', 'index': ['1026', '1']}
        result = toc.toc_sect_appendix(data, [])
        self.assertEqual(u'1026.1', result['label'])
        self.assertEqual('Authority', result['sub_label'])
        self.assertTrue(result['is_section'])

        data = {'title': u'§ 1026.1 [Reserved]', 'index': ['1026', '1']}
        result = toc.toc_sect_appendix(data, [])
        self.assertEqual(u'1026.1', result['label'])
        self.assertEqual('[Reserved]', result['sub_label'])
        self.assertTrue(result['is_section'])

        data = {'title': u'Appendix A', 'index': ['1026', 'A']}
        result = toc.toc_sect_appendix(data, [])
        self.assertEqual('Appendix A', result['label'])
        self.assertTrue(result['is_first_appendix'])
        self.assertTrue(result['is_appendix'])

        data = {'title': u'Appendix B [Reserved]', 'index': ['1026', 'A']}
        result = toc.toc_sect_appendix(data, [])
        self.assertEqual('Appendix B', result['label'])
        self.assertEqual('[Reserved]', result['sub_label'])
        self.assertTrue(result['is_first_appendix'])
        self.assertTrue(result['is_appendix'])

        data = {'title': u'Appendix B [Reserved]', 'index': ['1026', 'A']}
        result = toc.toc_sect_appendix(data, [{'is_appendix': True}])
        self.assertEqual('Appendix B', result['label'])
        self.assertEqual('[Reserved]', result['sub_label'])
        self.assertFalse(result['is_first_appendix'])
        self.assertTrue(result['is_appendix'])

    def test_toc_subpart(self):
        layer = {'1001-Subpart-A': [{'title': '1001.1 - Content',
                                     'index': ['1001', '1']},
                                    {'title': '1001.2 - Other',
                                     'index': ['1001', '2']}]}
        data = {'title': u'General', 'index': ['1001', 'Subpart', 'A']}
        result = toc.toc_subpart(data, [], layer)
        self.assertEqual('Subpart A', result['label'])
        self.assertEqual('General', result['sub_label'])
        self.assertEqual(['1001', 'Subpart', 'A'], result['index'])
        self.assertEqual('1001-Subpart-A', result['section_id'])
        self.assertTrue(result.get('is_subpart'))
        self.assertEqual(2, len(result['sub_toc']))

        s1, s2 = result['sub_toc']
        self.assertEqual('Content', s1['sub_label'])
        self.assertEqual(['1001', '1'], s1['index'])
        self.assertEqual('Other', s2['sub_label'])
        self.assertEqual(['1001', '2'], s2['index'])

    def test_toc_subpart_reserved(self):
        layer = {'1001-Subpart-A': [{'title': '1001.1 - Content',
                                     'index': ['1001', '1']},
                                    {'title': '1001.2 - Other',
                                     'index': ['1001', '2']}]}
        data = {'title': u'[Reserved]', 'index': ['1001', 'Subpart', 'B']}
        result = toc.toc_subpart(data, [], layer)
        self.assertEqual('Subpart B', result['label'])
        self.assertEqual('[Reserved]', result['sub_label'])
        self.assertEqual(['1001', 'Subpart', 'B'], result['index'])
        self.assertEqual('1001-Subpart-B', result['section_id'])
        self.assertTrue(result.get('is_subpart'))
        self.assertEqual(0, len(result['sub_toc']))

    def test_toc_interp(self):
        so_far = [
            {'index': ['1001', '1']},
            {'index': ['1001', '2']},
            {'index': ['1001', 'A'], 'is_appendix': True},
            {'index': ['1001', 'B'], 'is_appendix': True}]
        data = {'title': 'Supplement II - Official Interps',
                'index': ['1001', 'Interp']}
        toc_data = {'1001-Interp': []}
        result = toc.toc_interp(data, so_far, toc_data)
        self.assertEqual('Supplement II', result['label'])
        self.assertEqual('Official Interps', result['sub_label'])
        self.assertTrue(result.get('is_supplement'))
        self.assertEqual(2, len(result['sub_toc']))

        reg, app = result['sub_toc']
        self.assertEqual('Regulation Text', reg['label'])
        self.assertTrue(reg.get('is_subterp'))
        self.assertEqual(['1001', 'Subpart', 'Interp'], reg['index'])
        self.assertEqual('1001-Subpart-Interp', reg['section_id'])

        self.assertEqual('Appendices', app['label'])
        self.assertTrue(app.get('is_subterp'))
        self.assertEqual(['1001', 'Appendices', 'Interp'], app['index'])
        self.assertEqual('1001-Appendices-Interp', app['section_id'])

        so_far = [
            {'index': ['1001', 'Subpart', 'C'], 'is_subpart': True,
             'label': 'Subpart C', 'sub_label': 'Awesome Sauce',
             'sub_toc': [{'index': ['1001', '1']}, {'index': ['1001', '2']}]}]
        data = {'title': 'Unparsable',
                'index': ['1001', 'Interp']}
        result = toc.toc_interp(data, so_far, toc_data)
        self.assertEqual('Supplement I', result['label'])
        self.assertEqual('', result['sub_label'])
        self.assertTrue(result.get('is_supplement'))
        self.assertEqual(1, len(result['sub_toc']))

        subpart = result['sub_toc'][0]
        self.assertEqual('Subpart C', subpart['label'])
        self.assertEqual('Awesome Sauce', subpart['sub_label'])
        self.assertTrue(subpart.get('is_subterp'))
        self.assertEqual(['1001', 'Subpart', 'C', 'Interp'], subpart['index'])
        self.assertEqual('1001-Subpart-C-Interp', subpart['section_id'])

        toc_data = {'1001-Interp': [{'title': 'Intro',
                                     'index': ['1001', 'Interp', 'h1']},
                                    {'title': 'Section 1',
                                     'index': ['1001', '1', 'Interp']}]}
        result = toc.toc_interp(data, so_far, toc_data)
        self.assertEqual(2, len(result['sub_toc']))

        h1, subpart = result['sub_toc']
        self.assertEqual('Interpretations', h1['label'])
        self.assertEqual('Intro', h1['sub_label'])
        self.assertFalse(h1.get('is_subterp', False))
        self.assertEqual('1001-Interp-h1', h1['section_id'])
        self.assertEqual(['1001', 'Interp', 'h1'], h1['index'])
        self.assertTrue(subpart.get('is_subterp'))
        self.assertEqual(['1001', 'Subpart', 'C', 'Interp'], subpart['index'])
        self.assertEqual('1001-Subpart-C-Interp', subpart['section_id'])
