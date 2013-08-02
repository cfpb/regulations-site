from unittest import TestCase
from mock import Mock, patch

from regulations.generator.layers.layers_applier import *
from regulations.views.chrome import *

class ViewTests(TestCase):
    def test_build_context(self):
        builder = HTMLBuilder(InlineLayersApplier(), 
                ParagraphLayersApplier(), 
                SearchReplaceLayersApplier())

        context = {'reg_part':''}
        new_context = build_context(context, builder)
        self.assertEquals(new_context.keys(), ['GOOGLE_ANALYTICS_ID', 'tree', 'env', 
                                                'reg_part', 'GOOGLE_ANALYTICS_SITE'])
    def test_generate_html(self):
        regulation_tree = {'text': '', 'children': [], 'label': ['8675'],
            'title': 'Regulation R'
        }
        i_applier = InlineLayersApplier()
        p_applier = ParagraphLayersApplier()
        sr_applier = SearchReplaceLayersApplier()
        appliers = (i_applier, p_applier, sr_applier)
        builder = generate_html(regulation_tree, appliers)
        self.assertEquals(builder.tree, regulation_tree)
        self.assertEquals(builder.inline_applier, i_applier)
        self.assertEquals(builder.p_applier, p_applier)
        self.assertEquals(builder.search_applier, sr_applier)
