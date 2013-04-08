import urllib

class ExternalCitationLayer():
    def __init__(self, layer):
        self.layer = layer

    @staticmethod
    def generate_fdsys_href_tag(text, parameters):
        """ Generate an href tag to FDSYS. """
        parameters['year'] = "mostrecent"
        parameters['link-type'] = "html"

        fdsys_url_base = "http://api.fdsys.gov/link"
        fdsys_url = "%s?%s" % (fdsys_url_base, urllib.urlencode(parameters))
        tag = '<a href="%s">%s</a>' % (fdsys_url, text)
        return tag

    @staticmethod
    def generate_cfr_link(text, citation):
        """ Convert the CFR references into an HTML <a href> tag. """
        parameters = {'title':citation[0], 'chapter':citation[1]}
        if len(citation) > 2:
            parameters['section'] = citation[2]

        parameters['collection'] = 'cfr'
        return ExternalCitationLayer.generate_fdsys_href_tag(text, parameters)

    @staticmethod
    def generate_uscode_link(text, citation):
        """ Convert the US Code references into an HTML <a href> tag. """
        parameters = {"collection":"uscode", 
                      "title":citation[0],
                      "section":citation[1]}
        return ExternalCitationLayer.generate_fdsys_href_tag(text, parameters)

    @staticmethod
    def create_link(text, layer_element):
        if layer_element['citation_type'] == 'USC':
            generator = ExternalCitationLayer.generate_uscode_link
        elif layer_element['citation_type'] == 'CFR':
            generator = ExternalCitationLayer.generate_cfr_link
        return generator(text, layer_element['citation'])

    def apply_layer(self, text, text_index):
        if text_index in self.layer:
            layer_elements = self.layer[text_index]

            layer_pairs = []
            for layer_element in layer_elements:
                for start, end in layer_element['offsets']:
                    ot = text[int(start):int(end)]
                    rt = ExternalCitationLayer.create_link(ot, layer_element)
                    layer_pairs.append((ot, rt))
                return layer_pairs
