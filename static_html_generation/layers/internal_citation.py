from django.template import loader, Context

class InternalCitationLayer():
    def __init__(self, layer):
        self.layer = layer

    @staticmethod
    def create_link(text, layer_element):
        template =  loader.get_template('internal_citation.html')

        citation_url = "-".join(layer_element['citation'])
        citation = {'url': citation_url, 
                    'label':text}

        c = Context({'citation':citation})
        return template.render(c).strip('\n')

    def apply_layer(self, text, text_index):    
        if text_index in self.layer:
            layer_elements = self.layer[text_index]

            layer_pairs = []
            for layer_element in layer_elements:
                for start, end in layer_element['offsets']:
                    ot = text[int(start):int(end)]
                    rt = InternalCitationLayer.create_link(ot, layer_element)
                    layer_pairs.append((ot, rt))
            return layer_pairs
