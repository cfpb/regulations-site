from django.http import HttpRequest

#   Don't import PartialInterpView directly; this will cause an import cycle
from regulations import views
from regulations.generator.node_types import label_to_text, to_markup_id


class InterpretationsLayer(object):
    """Fetches the (rendered) interpretation for this node, if available"""
    shorthand = 'interp'

    def __init__(self, layer, version=None):
        self.layer = layer
        self.version = version

    def apply_layer(self, text_index):
        """Return a pair of field-name + interpretation if one applies."""
        if text_index in self.layer and self.layer[text_index]:
            context = {'interps': [], 
                       'for_markup_id': text_index,
                       'for_label': label_to_text(text_index.split('-'),
                                                  include_section=False)}
            for layer_element in self.layer[text_index]:
                reference = layer_element['reference']

                partial_view = views.partial.PartialInterpView.as_view(
                    inline=True)
                request = HttpRequest()
                request.GET['layers'] = 'terms,internal,keyterms,paragraph'
                request.method = 'GET'
                response = partial_view(request, label_id=reference,
                                        version=self.version)
                response.render()

                interp = {
                    'label_id': reference,
                    'markup': response.content,
                }

                #  exclude 'Interp'
                ref_parts = reference.split('-')[:-1]
                interp['section_id'] = '%s-Interp' % ref_parts[0]

                context['interps'].append(interp)

            return 'interp', context
