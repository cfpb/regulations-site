from django.conf import settings
from django.views.generic.base import TemplateView
from regulations.generator import generator
from regulations.generator.html_builder import HTMLBuilder

def generate_html(regulation_tree, layer_appliers):
    builder = HTMLBuilder(*layer_appliers)
    builder.tree = regulation_tree
    builder.generate_html()
    return builder

def build_context(context, builder):
    """ Populate a context given an HTMLBuilder object. """
    context['tree'] = builder.tree
    context['env'] = builder.get_env_dir()
    context['GOOGLE_ANALYTICS_SITE'] = settings.GOOGLE_ANALYTICS_SITE
    context['GOOGLE_ANALYTICS_ID'] = settings.GOOGLE_ANALYTICS_ID
    return context

class RegulationView(TemplateView):
    """ Display the whole regulation text as one page, with all the chrome elements. """
    template_name = 'simpler.html'

    def get_context_data(self, **kwargs):
        context = super(RegulationView, self).get_context_data(**kwargs)

        regulation_part = context['reg_part']
        regulation_version = context['reg_version']

        appliers = generator.get_all_layers(regulation_part, regulation_version)
        tree = generator.get_regulation(regulation_part, regulation_version)

        builder = generate_html(tree, appliers)
        context = build_context(context, builder)
        return context

class RegulationSectionView(TemplateView):
    """ Display a single section of the regulation as one page, with all the chrome elements. """
    template_name = 'simpler.html'

    @staticmethod
    def get_regulation_part(reg_part_section):
        if '-' in reg_part_section:
            return reg_part_section.split('-')[0]
        else:
            return reg_part_section

    def get_context_data(self, **kwargs):
        context = super(RegulationSectionView, self).get_context_data(**kwargs)

        regulation_part = context['reg_part_section']
        regulation_version = context['reg_version']

        regulation = RegulationSectionView.get_regulation_part(context['reg_part_section'])
        inline_applier, p_applier, s_applier = generator.get_all_section_layers(regulation_part, regulation_version)

        #The table of contents layers are dealt with different for section at a time. 
        p_applier = generator.add_full_toc(regulation, regulation_version, p_applier)
        inline_applier = generator.add_section_internal_citations(regulation, regulation_version, inline_applier)

        section_tree = generator.get_regulation_section(regulation, 
                            regulation_version, context['reg_part_section'])

        builder = generate_html(section_tree, (inline_applier, p_applier, s_applier))
        context = build_context(context, builder)
        return context

class RegulationParagraphView(TemplateView):
    """ Display a single paragraph of a regulation with all the chrome elements. """
    template_name = "tree.html"

    def get_context_data(self, **kwargs):
        context = super(RegulationParagraphView,
                self).get_context_data(**kwargs)

        paragraph_id = context['paragraph_id']
        version = context['reg_version']

        appliers = generator.get_all_section_layers(paragraph_id, version)
        paragraph_tree = generator.get_tree_paragraph(paragraph_id, version)

        builder = generate_html(paragraph_tree, appliers)

        context['node'] = builder.tree
        return context
