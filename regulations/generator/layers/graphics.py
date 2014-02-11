from django.template import loader
import utils


class GraphicsLayer(object):
    shorthand = 'graphics'

    def __init__(self, layer_data):
        self.layer_data = layer_data
        self.template = loader.get_template('regulations/layers/graphics.html')

    def apply_layer(self, text_index):
        """Replace all instances of graphics with an img tag"""
        layer_pairs = []
        if text_index in self.layer_data:
            for graphic_info in self.layer_data[text_index]:

                context = {
                    'url': graphic_info['url'],
                    'alt': graphic_info['alt']
                }

                if 'thumb_url' in graphic_info:
                    context['thumb_url'] = graphic_info['thumb_url']

                replacement = utils.render_template(self.template, context)
                layer_pairs.append((
                    graphic_info['text'], replacement,
                    graphic_info['locations']))
        return layer_pairs
