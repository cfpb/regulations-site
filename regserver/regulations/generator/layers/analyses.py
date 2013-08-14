class SectionBySectionLayer(object):
    def __init__(self, layer):
        self.layer = layer

    def apply_layer(self, text_index):
        """Return a pair of field-name + analyses if they apply"""
        if text_index in self.layer and self.layer[text_index]:
            references = []
            for layer_element in self.layer[text_index]:
                references.append(layer_element['reference'])

            return 'analyses', references
