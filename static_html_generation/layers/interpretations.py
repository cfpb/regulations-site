from django.template import loader, Context

class InterpretationsLayer(object):
    def __init__(self, layer):
        self.layer = layer

    def apply_layer(self, text, text_index):
        if text_index in self.layer:
            for layer_element in self.layer[text_index]:
                reference = layer_element['reference']

                template = loader.get_template('interpretation_ref.html')
                context = Context({
                    "interpretation_ref": reference,
                    "paragraph_text": text
                    })
                rendered = template.render(context).strip('\n')

                return[(text, rendered)]    # replace whole paragraph
