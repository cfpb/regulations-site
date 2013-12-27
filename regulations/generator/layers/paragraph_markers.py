from django.template import loader
import utils

class ParagraphMarkersLayer(object):
    shorthand = 'paragraph'

    def __init__(self, layer):
        self.layer = layer
        self.template = loader.get_template(
            'regulations/layers/paragraph_markers.html')

    def apply_layer(self, text_index):
        elements = []
        if text_index in self.layer:
            for layer_element in self.layer[text_index]:
                to_replace = layer_element['text']
                stripped = to_replace.replace('(', '').replace(')', '')
                stripped = stripped.replace('.', '')

                context = {'paragraph': to_replace,
                           'paragraph_stripped': stripped}
                replace_with = utils.render_template(self.template, context)
                elements.append(
                    (to_replace, replace_with, layer_element['locations']))
        return elements
