from unittest import TestCase
from datetime import datetime

from mock import Mock, patch

from regulations.generator import notices


class NoticesTest(TestCase):

    def test_fetch_all(self):
        api = Mock()
        api.notices.return_value = {"results": [
            {"document_number": "1234"}, {"document_number": "9898"}
        ]}
        #   Would normally return a notice object
        api.notice.side_effect = lambda d_num: d_num + d_num

        self.assertEqual(["12341234", "98989898"], notices.fetch_all(api))

    @patch('regulations.generator.notices.loader.get_template')
    @patch('regulations.generator.notices.sxs_markup')
    def test_markup(self, sxs_markup, get_template):
        get_template.return_value.render.return_value = '[html]'
        sxs_markup.return_value = '[sxs-html]'

        notices.markup({
            'cfr_part': '2222',
            'document_number': '888-2222',
            'section_by_section': [
                'child1',
                'child2',
                'child3'
            ]
        })
        self.assertEqual(3, sxs_markup.call_count)  # per child
        self.assertEqual('child1', sxs_markup.call_args_list[0][0][0])
        self.assertEqual('child2', sxs_markup.call_args_list[1][0][0])
        self.assertEqual('child3', sxs_markup.call_args_list[2][0][0])

        context = get_template.return_value.render.call_args[0][0]
        self.assertEqual('2222', context['cfr_part'])
        self.assertEqual('888-2222', context['document_number'])
        #   get the markup for children
        self.assertEqual([
            '[sxs-html]', '[sxs-html]', '[sxs-html]'],
            context['sxs_markup'])

    def test_sxs_markup(self):
        template = Mock()
        template.render.return_value = "[html]"

        sxs = {
            "label": "999-22",
            "paragraphs": ["P1", "P2"],
            "title": "999-22 Title",
            "children": [{
                "paragraphs": ["p1"],
                "title": "Some Other Title",
                "children": []
            }]
        }
        notices.sxs_markup(sxs, 2, template)
        #   One call in the child, one in the parent
        self.assertEqual(2, len(template.render.call_args_list))

        child_render_context = template.render.call_args_list[0][0][0]
        self.assertEqual(['p1'], child_render_context['paragraphs'])
        self.assertEqual('Some Other Title', child_render_context['title'])
        self.assertEqual(3, child_render_context['depth'])
        self.assertEqual([], child_render_context['children'])

        parent_context = template.render.call_args_list[1][0][0]
        self.assertEqual(['P1', 'P2'], parent_context['paragraphs'])
        self.assertEqual('999-22 Title', parent_context['title'])
        self.assertEqual(2, parent_context['depth'])
        self.assertEqual('999-22', parent_context['label'])
        #   Replaced children with their markup
        self.assertEqual(['[html]'], parent_context['children'])

    def test_find_label_in_sxs_found(self):
        sxs_list = [
            {'label': '204-1', 'children': []},
            {'label': '204-2', 'children': [{
                'label': '204-2-a',
                'children': [],
                'paragraphs': ['abc']}]}]

        s = notices.find_label_in_sxs(sxs_list, '204-2-a')
        self.assertEqual({
            'label': '204-2-a', 'children': [],
            'paragraphs': ['abc']}, s)

    def test_non_empty_sxs(self):
        sxs = {'label': '204-2-a', 'children': [], 'paragraphs': ['abc']}
        self.assertTrue(notices.non_empty_sxs(sxs))

    def test_non_empty_sxs_no_paragraph(self):
        sxs = {'label': '204-2-a', 'children': [], 'paragraphs': []}
        self.assertFalse(notices.non_empty_sxs(sxs))

    def test_non_empty_sxs_has_children(self):
        sxs = {
            'label': '204-2-a',
            'children': [{'title': 'abc'}],
            'paragraphs': []}
        self.assertTrue(notices.non_empty_sxs(sxs))

    def test_find_label_in_sxs_not_found(self):
        sxs_list = [
            {'label': '204-1', 'children': []},
            {'label': '204-2', 'children': [{
                'label': '204-2-a',
                'children': []}]}]

        s = notices.find_label_in_sxs(sxs_list, '202-a')
        self.assertEqual(None, s)

    def test_filter_children(self):
        sxs = {'children': [
            {'label': '204-a', 'paragraphs': ['me']},
            {'paragraphs': ['abcd']}]}
        filtered = notices.filter_labeled_children(sxs)
        self.assertEqual(filtered, [{'paragraphs': ['abcd']}])

    def test_filter_children_no_candidates(self):
        sxs = {'children': [
            {'label': '204-a', 'paragraphs': ['me']},
            {'label': '204-b', 'paragraphs': ['abcd']}]}
        filtered = notices.filter_labeled_children(sxs)
        self.assertEqual(filtered, [])

    def test_add_depths(self):
        sxs = {
            'label': '204-2',
            'children': [{
                'label': '204-2-a',
                'children': [],
                'paragraphs': ['abc']}]}
        notices.add_depths(sxs, 3)
        depth_sxs = {
            'label': '204-2',
            'depth': 3,
            'children': [{
                'depth': 4,
                'label': '204-2-a',
                'children': [],
                'paragraphs': ['abc']}]}
        self.assertEqual(depth_sxs, sxs)

    def test_extract_metdata(self):
        notice = {
            'action':'final rule', 
            'document_number':'204-1234',
            'fr_url': 'http://example.com', 
            'publication_date':'2013-09-12', 
            'effective_on':'2013-10-28', 
            'regulation_id_numbers': ['205', '204'], 
            'section_by_section':{'paragraphs':[]}
            }
        extracted = notices.extract_notice_metadata(notice)

        self.assertEqual(extracted['action'], 'final rule')
        self.assertEqual(extracted['document_number'], '204-1234')
        self.assertEqual(extracted['fr_url'], 'http://example.com')
        self.assertEqual(extracted['regulation_id_numbers'], ['205', '204'])

        pub_date = datetime.strptime('2013-09-12', "%Y-%m-%d") 
        effective_date = datetime.strptime('2013-10-28', "%Y-%m-%d")
        self.assertEqual(extracted['publication_date'], pub_date)
        self.assertEqual(extracted['effective_on'], effective_date)
