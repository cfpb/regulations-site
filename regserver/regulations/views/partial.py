from django.views.generic.base import TemplateView
from regulations.generator import generator
from regulations.generator.html_builder import HTMLBuilder

from regulations.views.chrome import RegulationSectionView, generate_html, build_context
from regulations.views import utils

class PartialSectionView(TemplateView):
    template_name = 'regulation-content.html'

    def get_context_data(self, **kwargs):
        context = super(PartialSectionView, self).get_context_data(**kwargs)

        regulation_part = context['reg_part_section']
        regulation_version = context['reg_version']

        regulation = RegulationSectionView.get_regulation_part(context['reg_part_section'])

        if 'layers' in self.request.GET.keys():
            inline_applier, p_applier, s_applier = utils.handle_specified_layers(self.request.GET['layers'], 
                    regulation_part, regulation_version, sectional=True)
        else:
            inline_applier, p_applier, s_applier = generator.get_all_section_layers(regulation_part, regulation_version)
            inline_applier = generator.add_section_internal_citations(regulation, regulation_version, inline_applier)

        section_tree = generator.get_tree_paragraph(regulation_part, regulation_version)
        builder = generate_html(section_tree, (inline_applier, p_applier, s_applier))
        context = build_context(context, builder)
        return context
        
class PartialParagraphView(TemplateView):
    """ Display a single paragraph of a regulation with all the chrome elements. """
    template_name = "tree.html"

    def get_context_data(self, **kwargs):

        context = super(PartialParagraphView,
                self).get_context_data(**kwargs)

        paragraph_id = context['paragraph_id']
        version = context['reg_version']

        if 'layers' in self.request.GET.keys():
            inline_applier, p_applier, s_applier = utils.handle_specified_layers(self.request.GET['layers'], 
                regulation, version)
        else:
            inline_applier, p_applier, s_applier = generator.get_all_section_layers(paragraph_id, version)
            inline_applier = generator.add_section_internal_citations(paragraph_id, version, inline_applier)

        paragraph_tree = generator.get_tree_paragraph(paragraph_id, version)
        builder = generate_html(paragraph_tree, (inline_applier, p_applier, s_applier))
        context['node'] = builder.tree
        return context
