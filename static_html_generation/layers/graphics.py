from django.template import loader, Context

class GraphicsLayer(object):
    def __init__(self, layer_data):
        self.layer_data = layer_data
        self.template = loader.get_template('graphics.html')

    def apply_layer(self, text_index):
        """Replace all instances of graphics with an img tag"""
        layer_pairs = []
        if text_index in self.layer_data:
            for graphic_info in self.layer_data[text_index]:
                context = Context({
                    'url': graphic_info['url'],
                    'alt': graphic_info['alt']
                })
                replacement = self.template.render(context).strip()
                layer_pairs.append((graphic_info['text'], replacement,
                    graphic_info['locations']))
        return layer_pairs
