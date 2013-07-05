from unittest import TestCase

from mock import Mock, patch

from regulations.generator.notices import *

class NoticesTest(TestCase):

    def test_fetch_all(self):
        api = Mock()
        api.notices.return_value = {"results": [
            {"document_number": "1234"}, {"document_number": "9898"}
        ]}
        #   Would normally return a notice object
        api.notice.side_effect = lambda d_num:d_num + d_num

        self.assertEqual(["12341234", "98989898"], fetch_all(api))

    @patch('regulations.generator.notices.loader.get_template')
    @patch('regulations.generator.notices.sxs_markup')
    def test_markup(self, sxs_markup, get_template):
        get_template.return_value.render.return_value = '[html]'
        sxs_markup.return_value = '[sxs-html]'

        markup({
            'cfr_part': '2222',
            'document_number': '888-2222',
            'section_by_section': [
                'child1',
                'child2',
                'child3'
            ]
        })
        self.assertEqual(3, sxs_markup.call_count) # per child
        self.assertEqual('child1', sxs_markup.call_args_list[0][0][0])
        self.assertEqual('child2', sxs_markup.call_args_list[1][0][0])
        self.assertEqual('child3', sxs_markup.call_args_list[2][0][0])

        context = get_template.return_value.render.call_args[0][0]
        self.assertEqual('2222', context['cfr_part'])
        self.assertEqual('888-2222', context['document_number'])
        #   get the markup for children
        self.assertEqual(['[sxs-html]', '[sxs-html]', '[sxs-html]'], 
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
        sxs_markup(sxs, 2, template)
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
