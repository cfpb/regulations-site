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


class SubterpView(PartialView):
    """Serves as the base class for subterm views of interpretations (i.e.
    the groupings by subpart, regtext, or appendices)"""
    template_name = "regulations/interpretations.html"
    def get_context_data(self, **kwargs):
        #   skip our parent
        context = super(PartialView, self).get_context_data(**kwargs)

        label_id = context['label_id']
        part = label_id.split('-', 1)[0]
        version = context['version']
        
        section_list = self.get_section_list(part, version, label_id)

        if not section_list:
            raise Http404

        context['c'] = {'node_type': node_types.INTERP,
                        'children': []}
        for section_toc in section_list:
            interp_label = '-'.join(section_toc['index'] + ['Interp'])
            tree = generator.get_tree_paragraph(interp_label, version)
            if tree is not None:    # Not all sections will have an interp
                inline_applier, p_applier, s_applier = self.determine_appliers(
                    interp_label, version)
                builder = generate_html(tree,
                                        (inline_applier, p_applier, s_applier))
                context['c']['children'].append(builder.tree)

        return context

    def get_section_list(self, part, version):
        raise NotImplemented


class EmptySubpartView(SubterpView):
    """Displays all interps of regtext"""
    def get_section_list(self, part, version, label_id):
        toc = utils.table_of_contents(part, version, True)
        parts_list = []
        for el in toc:
            if el.get('is_section'):
                parts_list.append(el)
        return parts_list

class AppendicesView(SubterpView):
    """Displays all interps of appendices"""
    def get_section_list(self, part, version, label_id):
        toc = utils.table_of_contents(part, version, True)
        parts_list = []
        for el in toc:
            if el.get('is_appendix'):
                parts_list.append(el)
        return parts_list


class SubpartView(SubterpView):
    """Displays interps of a subpart"""
    def get_section_list(self, part, version, label_id):
        label_list = label_id.split('-')
        trimmed = label_list[:-1]   # Strip "Interp"
        toc = utils.table_of_contents(part, version, True)

        subpart_toc = None
        for el in toc:
            if el['index'] == trimmed:
                subpart_toc = el

        if not subpart_toc:
            raise Http404

        return subpart_toc.get('sub_toc', [])
