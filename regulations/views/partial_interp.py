from django.http import Http404

from regulations.generator import generator, node_types
from regulations.views import utils
from regulations.views.partial import PartialView, generate_html


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


class PartialSubterpView(PartialView):
    """View of subterps - interpretations of whole subparts, regtext, or
    appendices"""
    template_name = "regulations/interpretations.html"
    def get_context_data(self, **kwargs):
        #   skip our parent
        context = super(PartialView, self).get_context_data(**kwargs)

        label_id = context['label_id']
        part = label_id.split('-', 1)[0]
        version = context['version']
        
        section_list = utils.subterp_expansion(version, label_id)

        if not section_list:
            raise Http404

        context['markup_page_type'] = 'reg-section'
        html_label = node_types.to_markup_id(label_id.split('-'))
        context['c'] = {'node_type': node_types.INTERP,
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
                context['c']['children'].append(builder.tree)

        return context
