from django.http import HttpRequest

#   Don't import PartialInterpView or utils directly; causes an import cycle
from regulations import generator, views
from regulations.generator.node_types import label_to_text
from regulations.generator.section_url import SectionUrl


class InterpretationsLayer(object):
    """Fetches the (rendered) interpretation for this node, if available"""
    shorthand = 'interp'

    def __init__(self, layer, version=None):
        self.layer = layer
        self.version = version
        self.section_url = SectionUrl()

    def preprocess_root(self, root_node):
        """To prevent a set of calls per interpretation, make a single call
        for the root interpretation (for the requested section/paragraph)"""
        generator.generator.get_tree_paragraph(
            '-'.join(root_node['label'] + ['Interp']), self.version)

    def apply_layer(self, text_index):
        """Return a pair of field-name + interpretation if one applies."""
        if text_index in self.layer and self.layer[text_index]:
            context = {'interps': [],
                       'for_markup_id': text_index,
                       'for_label': label_to_text(text_index.split('-'),
                                                  include_section=False)}
            for layer_element in self.layer[text_index]:
                reference = layer_element['reference']

                partial_view = views.partial_interp.PartialInterpView.as_view(
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

                ref_parts = reference.split('-')
                interp['section_id'] = self.section_url.interp(
                    ref_parts, self.version)

                context['interps'].append(interp)

            return 'interp', context
