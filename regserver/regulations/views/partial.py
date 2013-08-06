from django.conf import settings
from django.views.generic.base import TemplateView

from regulations.generator import generator
from regulations.generator.html_builder import HTMLBuilder
from regulations.views import utils

def generate_html(regulation_tree, layer_appliers):
    builder = HTMLBuilder(*layer_appliers)
    builder.tree = regulation_tree
    builder.generate_html()
    return builder


class PartialView(TemplateView):
    """Base class of various partial markup views"""

    def get_context_data(self, **kwargs):
        context = super(PartialView, self).get_context_data(**kwargs)

        label_id = context['label_id']
        version = context['version']

        if 'layers' in self.request.GET.keys():
            inline_applier, p_applier, s_applier = utils.handle_specified_layers(self.request.GET['layers'], 
                    label_id, version, sectional=True)
        else:
            inline_applier, p_applier, s_applier = generator.get_all_section_layers(label_id, version)
            inline_applier = generator.add_section_internal_citations(label_id, 
                    version, inline_applier)

        tree = generator.get_tree_paragraph(label_id, version)
        builder = generate_html(tree, (inline_applier, p_applier, s_applier))

        return self.transform_context(context, builder)


class PartialSectionView(PartialView):
    """ Single section of reg text """
    template_name = 'regulation-content.html'

    def transform_context(self, context, builder):
        context['tree'] = {'children': [builder.tree]}
        return context

        
class PartialParagraphView(PartialView):
    """ Single paragraph of a regtext """

    template_name = "tree.html"

    def transform_context(self, context, builder):
        context['node'] = builder.tree
        return context


class PartialInterpView(PartialView):
    """ Interpretation of a reg text section/paragraph or appendix """

    template_name = "interpretations.html"

    def transform_context(self, context, builder):
        context['c'] = {'node_type': 'interp', 'children': [builder.tree]}
        return context


class PartialRegulationView(PartialView):
    """ Entire regulation without chrome """

    template_name = 'regulation-content.html'

    def transform_context(self, context, builder):
        context['tree'] = builder.tree
        return context
