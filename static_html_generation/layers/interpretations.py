from django.template import loader, Context
from node_types import NodeTypes

class InterpretationsLayer(object):
    def __init__(self, layer):
        self.layer = layer

    def apply_layer(self, text_index):
        """Return a pair of field-name + interpretation if one applies."""
        if text_index in self.layer and self.layer[text_index]:
            layer_element = self.layer[text_index][0]
            reference = layer_element['reference']
            reference = reference.split('-')
            reference = '-'.join(NodeTypes().change_type_names(reference))

            return 'interpretations', reference
