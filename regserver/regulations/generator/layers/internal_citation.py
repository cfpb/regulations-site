from django.template import loader, Context
from django.core.urlresolvers import reverse, NoReverseMatch
from ..node_types import to_markup_id

from regulations.generator.layers.utils import RegUrl


class InternalCitationLayer():
    shorthand = 'internal'

    def __init__(self, layer):
        self.layer = layer
        self.sectional = False
        self.version = None
        self.rev_urls = RegUrl()

    def render_url(
        self, label, text,
            template_name='layers/internal_citation.html'):

        url = self.rev_urls.fetch(label, self.version, self.sectional)
        c = Context({'citation': {'url': url, 'label': text}})
        template = loader.get_template(template_name)
        return template.render(c).strip('\n')

    def apply_layer(self, text, text_index):
        if text_index in self.layer:
            layer_elements = self.layer[text_index]

            layer_pairs = []
            for layer_element in layer_elements:
                for start, end in layer_element['offsets']:
                    ot = text[int(start):int(end)]
                    rt = self.render_url(layer_element['citation'], ot)
                    layer_pairs.append((ot, rt, (start, end)))
            return layer_pairs
