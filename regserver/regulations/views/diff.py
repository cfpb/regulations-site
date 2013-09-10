#vim: set encoding=utf-8
from django.views.generic.base import TemplateView
from django.http import Http404

from regulations.generator import generator
from regulations.generator.html_builder import HTMLBuilder
from regulations.generator.node_types import EMPTYPART, REGTEXT
from regulations.views import utils

def get_appliers(label_id, older, newer):
    diff = generator.get_diff_applier(label_id, older, newer)

    if diff is None:
        raise Http404

    appliers = utils.handle_specified_layers('graphics', label_id, older)
    appliers += (diff,)
    return appliers


class PartialSectionDiffView(TemplateView):
    """ A diff view of a partial section. """
    template_name = 'regulation-content.html'

    def get_context_data(self, **kwargs):
        context = super(
            PartialSectionDiffView, self).get_context_data(**kwargs)

        label_id = context['label_id']
        older = context['version']
        newer = context['newer_version']

        tree = generator.get_tree_paragraph(label_id, older)

        if tree is None:
            #TODO We need a more complicated check here to see if the diffs 
            #add the requested section. If not -> 404
            tree = {}

        appliers = get_appliers(label_id, older, newer)
        
        builder = HTMLBuilder(*appliers)
        builder.tree = tree
        builder.generate_html()

        child_of_root = builder.tree
        if builder.tree['node_type'] == REGTEXT:
            child_of_root = {
                'node_type': EMPTYPART,
                'children': [builder.tree]}
        context['tree'] = {'children': [child_of_root]}
        return context
