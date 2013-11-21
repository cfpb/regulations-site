import urllib
from django.template import loader
import utils


class ExternalCitationLayer():
    shorthand = 'external'

    def __init__(self, layer):
        self.layer = layer

    @staticmethod
    def generate_fdsys_href_tag(text, parameters):
        """ Generate an href tag to FDSYS. """
        parameters['year'] = "mostrecent"

        if 'link-type' not in parameters:
            parameters['link-type'] = "html"

        fdsys_url_base = "http://api.fdsys.gov/link"
        fdsys_url = "%s?%s" % (fdsys_url_base, urllib.urlencode(parameters))

        template = loader.get_template(
            'regulations/layers/external_citation.html')
        context = {
            'citation': {
                'url': fdsys_url,
                'label': text}}
        return utils.render_template(template, context)

    @staticmethod
    def generate_cfr_link(text, citation):
        """ Convert the CFR references into an HTML <a href> tag. """
        parameters = {'titlenum': citation[0], 'partnum': citation[1]}
        if len(citation) > 2:
            parameters['sectionnum'] = citation[2]

        parameters['link-type'] = 'xml'
        parameters['collection'] = 'cfr'
        return ExternalCitationLayer.generate_fdsys_href_tag(text, parameters)

    @staticmethod
    def generate_public_law_link(text, citation):
        """ Convert the Public Law references into an HTML <a href> tag. """
        parameters = {
            'congress': citation[0],
            'lawnum': citation[1],
            'collection': 'plaw',
            'lawtype': 'public'}
        return ExternalCitationLayer.generate_fdsys_href_tag(text, parameters)

    @staticmethod
    def generate_statutes_at_large_link(text, citation):
        parameters = {
            'statutecitation': '%s stat %s' % (citation[0], citation[2]),
            'collection': 'plaw'}
        return ExternalCitationLayer.generate_fdsys_href_tag(text, parameters)

    @staticmethod
    def generate_uscode_link(text, citation):
        """ Convert the US Code references into an HTML <a href> tag. """
        parameters = {
            "collection": "uscode",
            "title": citation[0],
            "section": citation[1]}
        return ExternalCitationLayer.generate_fdsys_href_tag(text, parameters)

    def citation_type_to_generator(self, citation_type):
        generator_map = {
            'USC': ExternalCitationLayer.generate_uscode_link,
            'CFR': ExternalCitationLayer.generate_cfr_link,
            'PUBLIC_LAW': self.generate_public_law_link,
            'STATUTES_AT_LARGE': self.generate_statutes_at_large_link
        }
        generator = generator_map[citation_type]
        return generator

    def create_link(self, text, layer_element):
        generator = self.citation_type_to_generator(
            layer_element['citation_type'])
        return generator(text, layer_element['citation'])

    def apply_layer(self, text, text_index):
        if text_index in self.layer:
            layer_elements = self.layer[text_index]

            layer_pairs = []
            for layer_element in layer_elements:
                for start, end in layer_element['offsets']:
                    ot = text[int(start):int(end)]
                    rt = self.create_link(ot, layer_element)
                    layer_pairs.append((ot, rt, (start, end)))
            return layer_pairs
