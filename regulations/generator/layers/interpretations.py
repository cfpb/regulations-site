from django.http import HttpRequest

#   Don't import PartialInterpView or utils directly; causes an import cycle
from regulations import views
from regulations.generator.node_types import label_to_text, to_markup_id


class InterpretationsLayer(object):
    """Fetches the (rendered) interpretation for this node, if available"""
    shorthand = 'interp'

    def __init__(self, layer, version=None):
        self.layer = layer
        self.version = version
        self.toc_cache = {}

    def determine_section_id(self, label):
        """Subterps add an annoying wrinkle to interpretation links. We have
        to figure out which subterp an interpretation is in, which is
        exactly what this method is for"""
        part = label[0]
        if self.version and len(label) > 2:
            key = (part, self.version)
            if key not in self.toc_cache:
                toc = views.utils.table_of_contents(part, self.version)
                self.toc_cache[key] = toc
            interpreted_section = label[:2]
            has_subparts = False
            for top in self.toc_cache[key]:
                if top['index'] == interpreted_section:
                    if top.get('is_section'):
                        return '%s-Subpart-Interp' % part
                    else:
                        return '%s-Appendices-Interp' % part

                for sub in top.get('sub_toc', []):
                    #   In a subpart
                    if sub['index'] == interpreted_section:
                        return '-'.join(top['index'] + ['Interp'])
        #   Default
        return '%s-Interp' % part

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
                interp['section_id'] = self.determine_section_id(ref_parts)

                context['interps'].append(interp)

            return 'interp', context
