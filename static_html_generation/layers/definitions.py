from django.template import loader, Context
from internal_citation import InternalCitationLayer

class DefinitionsLayer(object):
    def __init__(self, layer):
        self.layer = layer
        self.defining_template = loader.get_template('defining.html')

    def defined_terms(self, text, text_index):
        """Catch all terms which are defined elsewhere and replace them with
        a link"""
        layer_pairs = []
        if text_index in self.layer:
            layer_elements = self.layer[text_index]

            for layer_element in layer_elements:
                for start, end in layer_element['offsets']:
                    ot = text[int(start):int(end)]
                    ref_in_layer = layer_element['ref']
                    def_struct = self.layer['referenced'][ref_in_layer]

                    le = {'citation':def_struct['reference'].split('-')}
                    rt = InternalCitationLayer.create_link(ot, le, template_name='definition_citation.html')
                    layer_pairs.append((ot, rt, (start, end)))
        return layer_pairs

    def defining_terms(self, text, text_index):
        """Catch all terms which are defined in this paragraph, replace them
        with a span"""
        layer_pairs = []
        for ref_struct in self.layer['referenced'].values():
            if text_index == ref_struct['reference']:
                pos = tuple(ref_struct['position'])
                original = text[pos[0]:pos[1]]
                context = Context({'term': original})
                replacement = self.defining_template.render(context)
                replacement = replacement.strip('\n')
                layer_pairs.append((original, replacement, pos))
        return layer_pairs


    def apply_layer(self, text, text_index):
        return (self.defined_terms(text, text_index) 
                + self.defining_terms(text, text_index))
