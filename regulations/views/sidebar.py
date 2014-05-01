from django.views.generic.base import TemplateView
from django.http import Http404

from regulations.generator import api_reader
from regulations.generator.layers.analyses import SectionBySectionLayer
from regulations.generator.node_types import label_to_text
from regulations.generator.subterp import filter_by_subterp


class SideBarView(TemplateView):
    """ View for handling the right-side sidebar """
    def get_template_names(self):
        return ['regulations/custom-sidebar.html', 'regulations/sidebar.html']

    def add_sxs(self, client, node_trees, context):
        """Finds sxs associated with this section, adds them to the
        context"""
        version = context['version']
        label_id = context['label_id']
        if 'Interp' in label_id:
            reg_part = label_id.split('-')[0]
            sxs_layer_data = client.layer('analyses', reg_part + '-Interp',
                                          version)
        else:
            sxs_layer_data = client.layer('analyses', label_id, version)

        results = []
        result_key = None
        if sxs_layer_data:
            sxs_layer = SectionBySectionLayer(sxs_layer_data)
            for tree in node_trees:
                result = sxs_layer.apply_layer('-'.join(tree['label']))
                if result:
                    result_key = result[0]
                    results.extend(result[1])

        if result_key:
            context[result_key] = results

    def is_subterp(self, label):
        return ('Interp' in label and ('Subpart' in label
                                       or 'Appendices' in label))

    def _get_node_trees(self, client, label, version):
        """If using subterps, we might be getting a list of relevant trees
        rather than a single node."""
        tree_nodes = []
        if 'Interp' in label and ('Subpart' in label
                                  or 'Appendices' in label):
            #   Subterp
            interp = client.regulation(label[0] + '-Interp', version)
            if interp:
                tree_nodes = filter_by_subterp(interp['children'], label,
                                               version)
        else:
            node = client.regulation('-'.join(label), version)
            if node:
                tree_nodes.append(node)
        return tree_nodes

    def get_context_data(self, **kwargs):
        context = super(SideBarView, self).get_context_data(**kwargs)

        label = context['label_id'].split('-')
        context['human_label_id'] = label_to_text(label, include_marker=True)
        client = api_reader.ApiReader()

        node_trees = self._get_node_trees(client, label, context['version'])

        self.add_sxs(client, node_trees, context)

        return context
