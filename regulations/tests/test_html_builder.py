#vim: set encoding=utf-8
from unittest import TestCase
from mock import Mock

from regulations.generator.html_builder import *
from regulations.generator.layers.layers_applier import InlineLayersApplier
from regulations.generator.layers.layers_applier import ParagraphLayersApplier
from regulations.generator.node_types import REGTEXT, APPENDIX, INTERP
from regulations.generator.layers import diff_applier


class HTMLBuilderTest(TestCase):

    def test_process_node_appliers(self):
        node = {
            "text": "Text text text.",
            "children": [],
            "label": ["123", "aaa"],
            'node_type': REGTEXT
        }

        inline = Mock()
        inline.get_layer_pairs.return_value = []
        par = Mock()
        par.apply_layers.return_value = node
        sr = Mock()
        sr.get_layer_pairs.return_value = []
        sr.layers = {}

        builder = HTMLBuilder(inline, par, sr)
        builder.process_node(node)

        self.assertTrue(inline.get_layer_pairs.called)
        self.assertEqual("123-aaa",
                         inline.get_layer_pairs.call_args[0][0])
        self.assertEqual("Text text text.",
                         inline.get_layer_pairs.call_args[0][1])

        self.assertTrue(par.apply_layers.called)
        self.assertEqual(node, par.apply_layers.call_args[0][0])

    def test_header_parsing(self):
        builder = HTMLBuilder(None, None, None)

        node = {
            "label": ["234", "a", "1"],
            "title": "Title (Regulation R)",
            'node_type': APPENDIX
        }
        titleless_node = {
            "title": "Title",
            'node_type': REGTEXT
        }

        parsed_title = builder.parse_doc_title(node['title'])
        no_title = builder.parse_doc_title(titleless_node['title'])

        self.assertEqual("(Regulation R)", parsed_title)
        self.assertEqual(no_title, None)

    def test_list_level_interpretations(self):
        builder = HTMLBuilder(None, None, None)

        parts = ['101', '12', 'a', 'Interp', '1']
        node_type = INTERP

        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (1, '1'))

        parts.append('j')
        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (2, 'i'))

        parts.append('B')
        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (3, 'A'))

    def test_list_level_appendices(self):
        builder = HTMLBuilder(None, None, None)

        parts = ['101', 'A', '1', 'a']
        node_type = APPENDIX

        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (1, 'a'))

        parts.append('2')
        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (2, '1'))

        parts.append('k')
        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (3, 'i'))

        parts.append('B')
        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (4, 'A'))

    def test_list_level_regulations(self):
        builder = HTMLBuilder(None, None, None)

        parts = ['101', '1', 'a']
        node_type = REGTEXT

        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (1, 'a'))

        parts.append('2')
        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (2, '1'))

        parts.append('k')
        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (3, 'i'))

        parts.append('B')
        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (4, 'A'))

    def test_list_level_regulations_no_level(self):
        builder = HTMLBuilder(None, None, None)

        parts = ['101', '1']
        node_type = REGTEXT

        result = builder.list_level(parts, node_type)
        self.assertEquals(result, (None, None))

    def test_interp_node_with_citations(self):
        inline, p, sr = Mock(), Mock(), Mock()
        builder = HTMLBuilder(inline, p, sr)

        node = {
            'text': 'Interpretation with a link',
            'children': [],
            'node_type': INTERP,
            'label': ['999', '5', 'Interp']
        }
        p.apply_layers.return_value = node
        inline.get_layer_pairs.return_value = []
        sr.get_layer_pairs.return_value = []
        sr.layers = {}
        builder.process_node(node)
        layer_parameters = inline.get_layer_pairs.call_args[0]
        self.assertEqual('Interpretation with a link', layer_parameters[1])
        self.assertEqual('999-5-Interp', layer_parameters[0])

    def test_process_node_header(self):
        sr = Mock()
        sr.layers = {}
        builder = HTMLBuilder(None, ParagraphLayersApplier(), sr)
        node = {'text': '', 'children': [], 'label': ['99', '22'],
                'node_type': REGTEXT}
        builder.process_node(node)
        self.assertFalse('header' in node)

        node = {'text': '', 'children': [], 'label': ['99', '22'],
                'title': 'Some Title', 'node_type': REGTEXT}
        builder.process_node(node)
        self.assertTrue('header' in node)
        self.assertEqual('Some Title', node['header'])

        node = {'text': '', 'children': [], 'label': ['99', '22'],
                'title': u'§ 22.1 Title', 'node_type': REGTEXT}
        builder.process_node(node)
        self.assertTrue('header' in node)

    def test_no_section_sign(self):
        text = HTMLBuilder.section_space(' abc')
        self.assertEquals(text, ' abc')
        self.assertTrue(True)

    def test_modify_interp_node(self):
        node = {
            'node_type': INTERP,
            'label': ['872', '22', 'Interp'],
            'children': [{'label': ['872', '22', 'Interp', '1']},
                         {'label': ['872', '22', 'a', 'Interp']},
                         {'label': ['872', '22', 'b', 'Interp']}]
        }
        builder = HTMLBuilder(None, None, None)
        builder.modify_interp_node(node)
        self.assertTrue(node['section_header'])
        self.assertEqual(node['header_children'],
                         [{'label': ['872', '22', 'a', 'Interp']},
                          {'label': ['872', '22', 'b', 'Interp']}])
        self.assertEqual(node['par_children'],
                         [{'label': ['872', '22', 'Interp', '1']}])

        node['label'] = ['872', '222', 'a', 'Interp']
        builder.modify_interp_node(node)
        self.assertFalse(node['section_header'])

    def test_modify_interp_node_header(self):
        node = {
            'children': [],
            'header': 'This interprets 22(a), a paragraph',
            'label': ['872', '22', 'a', 'Interp'],
            'node_type': INTERP,
        }
        icl = InternalCitationLayer(None)
        icl.sectional = True
        ila = InlineLayersApplier()
        ila.add_layer(icl)
        builder = HTMLBuilder(ila, None, None)

        builder.modify_interp_node(node)
        self.assertEqual('This interprets '
                         + icl.render_url(['872', '22', 'a'], '22(a)')
                         + ', a paragraph', node['header_markup'])

        node['label'] = ['872', '22']
        builder.modify_interp_node(node)
        self.assertEqual(node['header'], node['header_markup'])

    def test_process_node_title_diff(self):
        builder = HTMLBuilder(None, None, None)
        diff = {'204': {'title': [('delete', 0, 2), ('insert', 4, 'AAC')],
                        'text':  [('delete', 0, 2), ('insert', 4, 'AAB')],
                        'op': ''}}
        da = diff_applier.DiffApplier(diff, None)
        node = {
            "label_id": "204",
            "title": "abcd",
            'node_type': APPENDIX
        }
        builder.diff_applier = da
        builder.process_node_title(node)
        self.assertEqual('<del>ab</del>cd<ins>AAC</ins>', node['header'])

    def test_process_node_title_section_space_diff(self):
        """" Diffs and sections spaces need to place nicely together. """
        builder = HTMLBuilder(None, None, None)
        diff = {'204': {'title': [('delete', 7, 9), ('insert', 10, 'AAC')],
                        'text':  [('delete', 0, 2), ('insert', 4, 'AAB')],
                        'op': ''}}
        da = diff_applier.DiffApplier(diff, None)
        node = {
            "label_id": u"204",
            "title": u"§ 101.6 abcd",
            'node_type': APPENDIX
        }
        builder.diff_applier = da
        builder.process_node_title(node)
        self.assertEqual(
            u'§&nbsp;101.6<del> a</del>b<ins>AAC</ins>cd', node['header'])

    def test_node_title_no_diff(self):
        builder = HTMLBuilder(None, None, None)
        node = {
            "label_id": "204",
            "title": "abcd",
            'node_type': APPENDIX
        }
        builder.process_node_title(node)
        self.assertTrue('header' in node)
        self.assertEqual(node['title'], 'abcd')

    def test_generate_html(self):
        exex = Mock(spec=[])        # no attributes
        p_applier = Mock()
        p_applier.layers = {'exex': exex}
        p_applier.apply_layers.side_effect = lambda n: n    # identity
        s_applier = Mock()
        s_applier.layers = {}
        builder = HTMLBuilder(None, p_applier, s_applier)
        builder.tree = {'label': ['1234'], 'children': [],
                        'node_type': 'regtext', 'text': ''}
        builder.generate_html()
        #   No explosion so far means this works for most layers

        exex = Mock()               # "includes" any attribute
        p_applier = Mock()
        p_applier.layers = {'exex': exex}
        p_applier.apply_layers.side_effect = lambda n: n    # identity
        builder = HTMLBuilder(None, p_applier, s_applier)
        builder.tree = {'label': ['1234'], 'children': [],
                        'node_type': 'regtext', 'text': ''}
        builder.generate_html()
        self.assertTrue(exex.preprocess_root.called)
        self.assertEqual(exex.preprocess_root.call_args[0][0],
                         builder.tree)
