from django.http import Http404

from regulations.generator import generator, node_types
from regulations.views import utils
from regulations.views.partial import (
    PartialSectionView, PartialView, generate_html)


class PartialInterpView(PartialView):
    """ Interpretation of a reg text section/paragraph or appendix. Used for
    in-line interpretations"""

    template_name = "regulations/interpretations.html"
    inline = False

    def transform_context(self, context, builder):
        context['inline'] = self.inline
        context['c'] = {'node_type': node_types.INTERP,
                        'children': [builder.tree]}
        return context


class PartialSubterpView(PartialSectionView):
    """View of subterps - interpretations of whole subparts, regtext, or
    appendices"""
    def get_context_data(self, **kwargs):
        #   skip our parent
        context = super(PartialView, self).get_context_data(**kwargs)

        label_id = context['label_id']
        part = label_id.split('-', 1)[0]
        version = context['version']

        context['navigation'] = self.section_navigation(label_id, version)

        section_list = utils.subterp_expansion(version, label_id)

        if not section_list:
            raise Http404

        context['markup_page_type'] = 'reg-section'
        html_label = node_types.to_markup_id(label_id.split('-'))
        interp_root = {'node_type': node_types.INTERP,
                       'children': [],
                       'html_label': html_label,
                       'markup_id': '-'.join(html_label)}
        for interp_label in section_list:
            tree = generator.get_tree_paragraph(interp_label, version)
            if tree is not None:    # Not all sections will have an interp
                inline_applier, p_applier, s_applier = self.determine_appliers(
                    interp_label, version)
                builder = generate_html(tree,
                                        (inline_applier, p_applier, s_applier))
                interp_root['children'].append(builder.tree)

        context['tree'] = {'children': [interp_root]}
        return context
