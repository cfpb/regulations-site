#vim: set encoding=utf-8
from django.views.generic.base import TemplateView
from django.http import Http404

from regulations.generator import generator
from regulations.generator.html_builder import HTMLBuilder
from regulations.generator.node_types import EMPTYPART, REGTEXT
from regulations.views import utils
from regulations.views.partial import generate_html
from regulations.generator.layers.diff_applier import DiffApplier


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

        reg = label_id.split('-')[0]
        diff = generator.get_diff_applier(reg, older, newer)

        if tree is None or diff is None:
            raise Http404

        appliers = utils.handle_specified_layers('', label_id, older)
        appliers += (diff)

        builder = HTMLBuilder(*appliers)
        builder.tree = tree
        builder.generate_html()

        # Add a tree layer to account for subpart if this is regtext
        child_of_root = builder.tree
        if builder.tree['node_type'] == REGTEXT:
            child_of_root = {
                'node_type': EMPTYPART,
                'children': [builder.tree]}
        context['tree'] = {'children': [child_of_root]}
        return context
