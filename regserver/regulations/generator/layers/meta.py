from regulations.generator.layers.utils import convert_to_python

class MetaLayer(object):
    shorthand = 'meta'

    def __init__(self, layer_data):
        self.layer_data = convert_to_python(layer_data)

    def apply_layer(self, text_index):
        """Return a pair of field-name (meta) + the layer data"""
        if text_index in self.layer_data and self.layer_data[text_index]:
            return 'meta', self.layer_data[text_index][0]
