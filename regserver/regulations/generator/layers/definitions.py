from django.template import loader, Context

from ..node_types import to_markup_id
import utils


class DefinitionsLayer(object):
    shorthand = 'terms'

    def __init__(self, layer):
        self.layer = layer
        self.defining_template = loader.get_template('layers/defining.html')
        self.citations_template =\
            loader.get_template('layers/definition_citation.html')
        self.sectional = False
        self.version = None
        self.rev_urls = utils.RegUrl()
        self.rendered = {}
        # precomputation 
        for def_struct in self.layer['referenced'].values():
            def_struct['reference_split'] = def_struct['reference'].split('-')

    def create_definition_link(self, original_text, citation):
        """ Create the link that takes you to the definition of the term. """
        key = (original_text, tuple(citation))
        if key not in self.rendered:
            context = {
                'citation': {
                    'url': self.rev_urls.fetch(citation, self.version,
                                           self.sectional),
                    'label': original_text,
                    'definition_reference': '-'.join(to_markup_id(citation))}}
            rendered =  utils.render_template(self.citations_template, context)
            self.rendered[key] = rendered
        return self.rendered[key]

    def defined_terms(self, text, text_index):
        """Catch all terms which are defined elsewhere and replace them with
        a link"""
        layer_pairs = []
        if text_index in self.layer:
            layer_elements = self.layer[text_index]

            for layer_element in layer_elements:
                ref = layer_element['ref']
                ref = self.layer['referenced'][ref]['reference_split']
                for start, end in layer_element['offsets']:
                    ot = text[start:end]
                    rt = self.create_definition_link(ot, ref)
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
