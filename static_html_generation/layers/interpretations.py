import api_reader
from html_builder import SlideDownInterpBuilder
from layers.layers_applier import ParagraphLayersApplier
from node_types import to_markup_id
import settings as app_settings

class InterpretationsLayer(object):
    def __init__(self, layer, version):
        self.layer = layer
        self.version = version

    def copy_builder(self, html_builder):
        self.builder = SlideDownInterpBuilder(html_builder.inline_applier,
            ParagraphLayersApplier(),
            html_builder.search_applier)

    def apply_layer(self, text_index):
        """Return a pair of field-name + interpretation if one applies."""
        if text_index in self.layer and self.layer[text_index]:
            layer_element = self.layer[text_index][0]
            reference = layer_element['reference']
            api = api_reader.Client(app_settings.API_BASE)
            interp_node = api.regulation(reference, self.version)

            if interp_node:
                interp_node['interp_for_markup_id'] = text_index
                reference_parts = reference.split('-')
                #   last two parts of the reference are section + paragraphs
                interp_node['interp_label'] = ''.join(reference_parts[-2:])
                self.builder.tree = interp_node
                self.builder.generate_html()
                markup = self.builder.render_markup()
                return 'interp', {
                    'markup': markup,
                    'markup_id': '-'.join(to_markup_id(reference_parts))
                }
