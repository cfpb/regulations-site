from django.template import loader, Context

class ParagraphMarkersLayer(object):
    def __init__(self, layer):
        self.layer = layer
        self.template = loader.get_template('paragraph_markers.html')

    def apply_layer(self, text_index):
        elements = []
        if text_index in self.layer:
            for layer_element in self.layer[text_index]:
                to_replace = layer_element['text']
                replace_with = self.template.render(
                    Context({'paragraph': to_replace})
                )
                elements.append(
                    (to_replace, replace_with, layer_element['locations']))
        return elements
