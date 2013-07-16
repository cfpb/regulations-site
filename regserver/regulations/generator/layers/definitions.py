from django.template import loader, Context
from ..node_types import to_markup_id
import utils

class DefinitionsLayer(object):
    def __init__(self, layer):
        self.layer = layer
        self.defining_template = loader.get_template('layers/defining.html')
        self.citations_template = loader.get_template('layers/definition_citation.html')

    @staticmethod
    def create_url(citation):
        """ Create the URL for a definition. """
        return '#' + '-'.join(to_markup_id(citation))

    @staticmethod
    def create_definition_reference(citation):
        """ Create a reference to a definition """
        return '-'.join(to_markup_id(citation))

    def create_definition_link(self, original_text, citation):
        """ Create the link that takes you to the definition of the term. """
        context = {'citation': {'url': DefinitionsLayer.create_url(citation), 
                    'label':original_text, 
                    'definition_reference': DefinitionsLayer.create_definition_reference(citation)}}
        return utils.render_template(self.citations_template, context)

    def create_layer_pair(self, text, offset, layer_element):
        """ Create a single layer pair. """
        start, end = offset
        ot = text[int(start):int(end)]
        ref_in_layer = layer_element['ref']
        def_struct = self.layer['referenced'][ref_in_layer]
        definition_reference = def_struct['reference'].split('-') 
        rt = self.create_definition_link(ot, definition_reference)
        return (ot, rt, (start, end))

    def defined_terms(self, text, text_index):
        """Catch all terms which are defined elsewhere and replace them with
        a link"""
        layer_pairs = []
        if text_index in self.layer:
            layer_elements = self.layer[text_index]

            for layer_element in layer_elements:
                for offset in layer_element['offsets']:
                    layer_pair = self.create_layer_pair(text, offset, layer_element)
                    layer_pairs.append(layer_pair)
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
