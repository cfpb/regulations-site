from django.views.generic.base import TemplateView
from django.http import Http404

from regulations.generator import api_reader, node_types
from regulations.generator.layers.analyses import SectionBySectionLayer
from regulations.generator.node_types import label_to_text
from regulations.views import utils


class SideBarView(TemplateView):
    """ View for handling the right-side sidebar """
    template_name = 'regulations/sidebar.html'

    def add_sxs(self, client, context):
        """Finds sxs associated with this section, adds them to the
        context"""
        version = context['version']
        result_key, results = None, []
        for label_id in utils.subterp_expansion(version, context['label_id']):
            sxs_layer_data = client.layer('analyses', label_id, version)

            if sxs_layer_data:
                sxs_layer = SectionBySectionLayer(sxs_layer_data)
                result = sxs_layer.apply_layer(label_id)
                if result:
                    result_key = result[0]
                    results.extend(result[1])

        if result_key:
            context[result_key] = results

    def add_permalinks(self, client, context):
        """Retrieves the whole reg and walks it, finding all of the labels.
        Adds them to the context"""
        version = context['version']
        context['permalinks'] = []

        def per_node(node):
            if node['node_type'] == node_types.INTERP:
                section_id = node['label'][0] + '-Interp'
            else:
                section_id = '-'.join(node['label'][:2])
            if len(node['label']) > 1:
                context['permalinks'].append({
                    'label_id': '-'.join(node['label']),
                    'section_id': section_id,
                    'text': label_to_text(node['label'], include_section=False,
                                          include_marker=True)
                })
            for child in node['children']:
                per_node(child)

        for label_id in utils.subterp_expansion(version, context['label_id']):
            reg = client.regulation(label_id, version)
            if reg:
                per_node(reg)

    def get_context_data(self, **kwargs):
        context = super(SideBarView, self).get_context_data(**kwargs)

        context['human_label_id'] = label_to_text(
            context['label_id'].split('-'), include_marker=True)
        client = api_reader.ApiReader()

        self.add_sxs(client, context)
        self.add_permalinks(client, context)

        return context
