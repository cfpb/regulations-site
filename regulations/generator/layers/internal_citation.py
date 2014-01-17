from django.template import loader, Context
from django.core.urlresolvers import reverse, NoReverseMatch
from ..node_types import to_markup_id

from regulations.generator.section_url import SectionUrl


class InternalCitationLayer():
    shorthand = 'internal'

    def __init__(self, layer):
        self.layer = layer
        self.sectional = False
        self.version = None
        self.rev_urls = SectionUrl()
        self.rendered = {}

    def render_url(
        self, label, text,
            template_name='regulations/layers/internal_citation.html'):

        key = (tuple(label), text, template_name)
        if key not in self.rendered:
            url = self.rev_urls.fetch(label, self.version, self.sectional)
            c = Context({'citation': {'url': url, 'label': text,
                'label_id': self.rev_urls.view_label_id(label, self.version)}})
            template = loader.get_template(template_name)
            self.rendered[key] = template.render(c).strip('\n')
        return self.rendered[key]

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
