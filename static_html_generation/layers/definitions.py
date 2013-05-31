from internal_citation import InternalCitationLayer

class DefinitionsLayer(object):
    def __init__(self, layer):
        self.layer = layer

    def get_definition_citation(self, definition_reference):
        return definition_reference.split(':')[1].split('-')
        
    def apply_layer(self, text, text_index):
        if text_index in self.layer:
            layer_elements = self.layer[text_index]

            layer_pairs = []
            for layer_element in layer_elements:
                for start, end in layer_element['offsets']:
                    ot = text[int(start):int(end)]
                    definition_ref = layer_element['ref']
                    definition_citation = self.get_definition_citation(definition_ref)

                    le  = {'citation':definition_citation}
                    rt = InternalCitationLayer.create_link(ot, le, template_name='definition_citation.html')
                    layer_pairs.append((ot, rt, (start, end)))
            return layer_pairs
