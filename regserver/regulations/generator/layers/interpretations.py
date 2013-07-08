from regulations.generator import api_reader
from regulations.generator.html_builder import SlideDownInterpBuilder
from regulations.generator.layers.layers_applier import ParagraphLayersApplier
from regulations.generator.node_types import to_markup_id
from django.conf import settings

class InterpretationsLayer(object):
    def __init__(self, layer, version):
        self.layer = layer
        self.version = version

    def copy_builder(self, html_builder):
        self.builder = SlideDownInterpBuilder(html_builder.inline_applier,
            ParagraphLayersApplier(),
            html_builder.search_applier)

    def copy_builder(self, inline_applier, search_applier):
        self.builder = SlideDownInterpBuilder(inline_applier,
            ParagraphLayersApplier(),
            search_applier)

    def apply_layer(self, text_index):
        """Return a pair of field-name + interpretation if one applies."""
        if text_index in self.layer and self.layer[text_index]:
            layer_element = self.layer[text_index][0]
            reference = layer_element['reference']
            api = api_reader.Client(settings.API_BASE)
            interp_node = api.regulation(reference, self.version)

            if interp_node:
                interp_node['interp_for_markup_id'] = text_index
                ref_parts = reference.split('-')
                if len(ref_parts) == 3:   # Part-Interp-Section/Appendix
                    interp_node['interp_label'] = ref_parts[2]
                elif ref_parts[2].isalpha(): # Part-Interp-Appendix-Segment
                    interp_node['interp_label'] = '-'.join(ref_parts[-2:])
                else: # Part-Interpretations-Section-Paragraphs
                    interp_node['interp_label'] = ''.join(ref_parts[-2:])
                self.builder.tree = interp_node
                self.builder.generate_html()
                markup = self.builder.render_markup()
                return 'interp', {
                    'markup': markup,
                    'markup_id': '-'.join(to_markup_id(ref_parts))
                }
