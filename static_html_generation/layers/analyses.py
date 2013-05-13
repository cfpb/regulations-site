from django.template import loader, Context

class SectionBySectionLayer(object):
    def __init__(self, layer):
        self.layer = layer

    def apply_layer(self, text, text_index):
        """Render the template for the whole paragraph. Creates one link per
        analyses."""
        if text_index in self.layer and self.layer[text_index]:
            references = []
            for layer_element in self.layer[text_index]:
                references.append(layer_element['reference'])
            
            template = loader.get_template('sxs_layer.html')
            context = Context({
                "references": references,
                "paragraph_text": text
                })
            rendered = template.render(context).strip('\n')

            return[(text, rendered)]    # replace whole paragraph
