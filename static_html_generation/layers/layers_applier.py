import json

class LayersApplier(object):
    """ Base class which keeps track of multiple laeyrs. """
    def __init__(self):
        self.layers = []

    def add_layer(self, layer):
        self.layers.append(layer)

class InlineLayersApplier(LayersApplier):
    """ Apply multiple inline layers to given text (e.g. links,
    highlighting, etc.) """
    def __init__(self):
        LayersApplier.__init__(self)
        self.original_text = None
        self.original_text_index = None
        self.modified_text = None

    def apply_layers(self, original_text, text_index):
        self.original_text = original_text
        self.modified_text = original_text
        self.original_text_index = text_index

        for layer in self.layers:
            layer_pairs = layer.apply_layer(self.original_text,
                    self.original_text_index)
            if layer_pairs:
                self.apply_pairs(layer_pairs)
        return self.modified_text

    def apply_pairs(self, pairs):
        """ Inline Layers return pairs of (search term, replacement text).
        Modify the text for each pair. """
        for old, new in pairs:
            self.modified_text = self.modified_text.replace(old, new)

class ParagraphLayersApplier(LayersApplier):
    """ Handle layers which apply to the whole paragraph. Layers include
    interpretations, section-by-section analyses, table of contents, etc."""

    def apply_layers(self, node):
        for layer in self.layers:
            pair = layer.apply_layer(node['markup_id'])
            if pair:
                node[pair[0]] = pair[1]
        return node
