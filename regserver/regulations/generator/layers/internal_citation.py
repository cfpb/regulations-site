from urlparse import urljoin
from django.template import loader, Context
from django.core.urlresolvers import reverse, NoReverseMatch
from ..node_types import to_markup_id

class InternalCitationLayer():
    def __init__(self, layer):
        self.layer = layer
        self.sectional = False
        self.version = None

    def render_url(self, label, text, template_name='layers/internal_citation.html'):
        if self.sectional:
            url = InternalCitationLayer.sectional_url_for(label, self.version)
        else:
            url = InternalCitationLayer.hash_url_for(label, self.version)
        c = Context({'citation': {'url': url, 'label': text}})
        template =  loader.get_template(template_name)
        return template.render(c).strip('\n')

    @staticmethod
    def sectional_url_for(label, version):
        section_url = '-'.join(to_markup_id(label[:2]))
        try:
            if 'Interp' in label and len(label) > 2:
                url = reverse('chrome_interp_view',
                        kwargs={'label_id':section_url + '-Interp', 
                            'version': version})
            else:
                url = reverse('chrome_section_view',
                        kwargs={'label_id':section_url, 'version': version})
        except NoReverseMatch:
            #XXX We have some errors in our layers. Once those are fixed, we 
            #need to revisit this. 
            url = ''
        return url + InternalCitationLayer.hash_url_for(label, version)

    @staticmethod
    def hash_url_for(label, version):
        return '#' + '-'.join(to_markup_id(label))


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
