from django.views.generic.base import TemplateView
from django.http import Http404

from regulations.generator import api_reader
from regulations.generator.layers.analyses import SectionBySectionLayer
from regulations.generator.node_types import label_to_text


class SideBarView(TemplateView):
    """ View for handling the right-side sidebar """
    template_name = 'sidebar.html'

    def get_context_data(self, **kwargs):
        context = super(SideBarView, self).get_context_data(**kwargs)

        label_id = context['label_id']
        version = context['version']

        client = api_reader.ApiReader()
        sxs_layer_data = client.layer('analyses', label_id, version)

        if sxs_layer_data is None:
            raise Http404

        sxs_layer = SectionBySectionLayer(sxs_layer_data)
        result = sxs_layer.apply_layer(label_id)
        if result:
            context[result[0]] = result[1]

        reg = client.regulation(label_id, version)

        if reg is None:
            raise Http404

        context['permalinks'] = []

        def per_node(node):
            if len(node['label']) > 1:
                context['permalinks'].append({
                    'label_id': '-'.join(node['label']),
                    'section_id': '-'.join(node['label'][:2]),
                    'text': label_to_text(node['label'], include_section=False,
                                          include_marker=True)
                })
            for child in node['children']:
                per_node(child)
        per_node(reg)

        return context
