import json

class LayersApplier(object):
    """ Apply multiple layers to a given text. """
    def __init__(self):
        self.layers = []
        self.original_text = None
        self.original_text_index = None
        self.modified_text = None

    def add_layer(self, layer):
        self.layers.append(layer)

    def apply_layer(self, layer):
        pairs = layer.apply_layer(self.original_text, self.original_text_index)
        return pairs

    def apply_pairs(self, pairs):
        for old, new in pairs:
            self.modified_text = self.modified_text.replace(old, new)

    def apply_layers(self, original_text, text_index):
        self.original_text = original_text
        self.modified_text = original_text
        self.original_text_index = text_index

        for layer in self.layers:
            pairs = self.apply_layer(layer)
            if pairs:
                self.apply_pairs(pairs)
        return self.modified_text
