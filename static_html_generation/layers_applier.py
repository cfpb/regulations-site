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
        layer.apply_layer(self.original_text, self.original_text_index)

    def apply_layers(self, original_text, text_index):
        self.original_text = original_text
        self.original_text_index = text_index

        for layer_location in self.layers:
            text = self.apply_layer(layer_location)
        return text
