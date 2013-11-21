from django.template import loader, Context


class DefinedLayer(object):
    shorthand = 'defined'

    def __init__(self, layer):
        self.layer = layer
        self.template = loader.get_template('regulations/layers/defining.html')

    def apply_layer(self, text, text_index):
        """Catch all terms which are defined in this paragraph, replace them
        with a span"""
        layer_pairs = []
        for ref_struct in self.layer['referenced'].values():
            if text_index == ref_struct['reference']:
                pos = tuple(ref_struct['position'])
                original = text[pos[0]:pos[1]]
                context = Context({'term': original})
                replacement = self.template.render(context)
                replacement = replacement.strip('\n')
                layer_pairs.append((original, replacement, pos))
        return layer_pairs
