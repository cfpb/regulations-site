from django.template import loader, Context

class InterpretationsLayer(object):
    def __init__(self, layer):
        self.layer = layer

    def apply_layer(self, text_index):
        """Return a pair of field-name + interpretation if one applies."""
        if text_index in self.layer and self.layer[text_index]:
            layer_element = self.layer[text_index][0]
            reference = layer_element['reference']

            return 'interpretations', reference
