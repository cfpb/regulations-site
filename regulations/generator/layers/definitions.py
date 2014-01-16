from django.template import loader, Context

from regulations.generator.section_url import SectionUrl
from ..node_types import to_markup_id
import utils


class DefinitionsLayer(object):
    shorthand = 'terms'

    def __init__(self, layer):
        self.layer = layer
        self.template = loader.get_template(
            'regulations/layers/definition_citation.html')
        self.sectional = False
        self.version = None
        self.rev_urls = SectionUrl()
        self.rendered = {}
        # precomputation
        for def_struct in self.layer['referenced'].values():
            def_struct['reference_split'] = def_struct['reference'].split('-')

    def create_definition_link(self, original_text, citation, term):
        """ Create the link that takes you to the definition of the term. """
        key = (original_text, tuple(citation))
        if key not in self.rendered:
            context = {
                'citation': {
                    'url': self.rev_urls.fetch(citation, self.version,
                                               self.sectional),
                    'label': original_text,
                    'term': term,
                    'definition_reference': '-'.join(to_markup_id(citation))}}
            rendered = utils.render_template(self.template, context)
            self.rendered[key] = rendered
        return self.rendered[key]

    def apply_layer(self, text, text_index):
        """Catch all terms which are defined elsewhere and replace them with
        a link"""
        layer_pairs = []
        if text_index in self.layer:
            layer_elements = self.layer[text_index]
            for layer_element in layer_elements:
                ref = layer_element['ref']
                # term = term w/o pluralization
                term = self.layer['referenced'][ref]['term']
                ref = self.layer['referenced'][ref]['reference_split']
                for start, end in layer_element['offsets']:
                    ot = text[start:end]
                    rt = self.create_definition_link(ot, ref, term)
                    layer_pairs.append((ot, rt, (start, end)))
        return layer_pairs
