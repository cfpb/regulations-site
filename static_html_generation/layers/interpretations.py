from django.template import loader, Context

class InterpretationsLayer(object):
    def __init__(self, layer):
        self.layer = layer

    def apply_layer(self, text, text_index):
        """Render the template for the whole paragraph. Assumes that there
        is only one interpretation applicable to a paragraph (for now)."""
        if text_index in self.layer and self.layer[text_index]:
            layer_element = self.layer[text_index][0]
            reference = layer_element['reference']

            template = loader.get_template('interpretation_ref.html')
            context = Context({
                "interpretation_ref": reference,
                "paragraph_text": text
                })
            rendered = template.render(context).strip('\n')

            return[(text, rendered)]    # replace whole paragraph
