from django.template import loader, Context
from html_builder import HTMLBuilder
from layers.layers_applier import InlineLayersApplier
from layers.layers_applier import ParagraphLayersApplier
from layers.layers_applier import SearchReplaceLayersApplier
from node_types import NodeTypes

class InterpretationsLayer(object):
    def __init__(self, layer):
        self.layer = layer
        self.template = loader.get_template('tree.html')

    def apply_layer(self, text_index, reg_tree):
        """Return a pair of field-name + interpretation if one applies."""
        if text_index in self.layer and self.layer[text_index]:
            layer_element = self.layer[text_index][0]
            reference = layer_element['reference']
            interp_node = self.find(reg_tree, reference)

            if interp_node:
                #   When we can generate paragraphs on demand, we should use
                #   that here
                builder = HTMLBuilder(InlineLayersApplier(),
                        ParagraphLayersApplier(reg_tree),
                        SearchReplaceLayersApplier())
                builder.process_node(interp_node)
                markup = self.template.render(Context({'node': interp_node}))
                return 'interp_markup', markup

    def find(self, reg_tree, index):
        """Find the matching node in the tree (if it exists)"""
        if reg_tree['label']['text'] == index:
            return reg_tree
        for child in reg_tree['children']:
            child_search = self.find(child, index)
            if child_search:
                return child_search
