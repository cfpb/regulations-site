import string
import utils
from django.template import loader, Context

class KeyTermsLayer(object):
    shorthand = 'keyterms'

    def __init__(self, layer):
        self.layer = layer
        self.template = loader.get_template('regulations/layers/key_term.html')

    def remove_punctuation(self, punctuated):
        translate_table = dict((ord(c), None) for c in string.punctuation)
        return punctuated.translate(translate_table)

    def generate_tag(self, key_term):
        key_term = {'key_term':key_term,
            'phrase':self.remove_punctuation(key_term)}
        context = {'key_term':key_term}
        return utils.render_template(self.template, context)

    def apply_layer(self, text_index):
        elements = []
        if text_index in self.layer:
            layer_elements = self.layer[text_index]

            for layer_element in layer_elements:
                key_term = layer_element['key_term'] 
                key_term_tag = self.generate_tag(key_term)
                locations = layer_element['locations']
                elements.append((key_term, key_term_tag, locations))
        return elements
