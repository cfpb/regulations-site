from django.conf import settings
from django.views.generic.base import TemplateView
from django.template import Context, loader

from regulations.generator import generator
from regulations.generator.html_builder import HTMLBuilder
from regulations.views import utils
from regulations.views.partial import *


def build_context(context, builder):
    """ Populate a context given an HTMLBuilder object. """
    context['tree'] = builder.tree
    context['env'] = builder.get_env_dir()
    context['GOOGLE_ANALYTICS_SITE'] = settings.GOOGLE_ANALYTICS_SITE
    context['GOOGLE_ANALYTICS_ID'] = settings.GOOGLE_ANALYTICS_ID
    return context

class RegulationView(TemplateView):
    """ Display the whole regulation text as one page, with all the chrome elements. """
    template_name = 'eregs-with-chrome.html'

    def get_context_data(self, **kwargs):
        context = super(RegulationView, self).get_context_data(**kwargs)

        reg_part = context['reg_part']
        reg_version = context['reg_version']

        if 'layers' in self.request.GET.keys():
            layer_names = self.request.GET['layers']
            appliers = utils.handle_specified_layers(layer_names, 
                        reg_part, reg_version)
        else:
            appliers = generator.get_all_layers(reg_part, reg_version)

        tree = generator.get_regulation(reg_part, reg_version)

        builder = generate_html(tree, appliers)
        context = build_context(context, builder)
        return context

class RegulationSectionView(TemplateView):
    """ Display a single section of the regulation as one page, with all the chrome elements. """
    template_name = 'eregs-with-chrome.html'

    @staticmethod
    def get_regulation_part(reg_part_section):
        if '-' in reg_part_section:
            return reg_part_section.split('-')[0]
        else:
            return reg_part_section

    def get_context_data(self, **kwargs):
        context = super(RegulationSectionView, self).get_context_data(**kwargs)

        reg_part_section = context['reg_part_section']
        reg_version = context['reg_version']

        regulation = RegulationSectionView.get_regulation_part(reg_part_section)

        if 'layers' in self.request.GET.keys():
            layer_names = self.request.GET['layers']
            inline_applier, p_applier, s_applier = utils.handle_specified_layers(layer_names, 
                        reg_part_section, reg_version, sectional=True)
        else:
            inline_applier, p_applier, s_applier = generator.get_all_section_layers(reg_part_section, reg_version)
            inline_applier = generator.add_section_internal_citations(regulation, reg_version, inline_applier)

        #The table of contents layers are dealt with different for section at a time. 
        p_applier = generator.add_full_toc(regulation, reg_version, p_applier)

        section_tree = generator.get_regulation_section(regulation, 
                            reg_version, context['reg_part_section'])

        builder = generate_html(section_tree, (inline_applier, p_applier, s_applier))
        context = build_context(context, builder)
        return context

class ChromeView(TemplateView):
    """ Base class for views which wish to include chrome. """
    template_name = 'chrome.html'

    def get_context_data(self, **kwargs):
        context = super(ChromeView, self).get_context_data(**kwargs)

        label_id = context['label_id']
        version = context['reg_version']

        if 'layers' in self.request.GET.keys():
            layer_names = self.request.GET['layers']
            appliers = utils.handle_specified_layers(layer_names, 
                        label_id, version)
        else:
            appliers = generator.get_all_layers(label_id, version)

        #   Hack solution: pull in full regulation
        #   @todo: just query the meta and toc layers
        full_tree = generator.get_regulation(label_id.split('-')[0],
                version)
        relevant_tree = generator.get_tree_paragraph(label_id, version)
        
        partial_view = PartialInterpView()
        partial_view.request = self.request
        partial_context = partial_view.get_context_data(label_id=label_id,
                reg_version=version)
        template = loader.get_template(PartialInterpView.template_name)

        context['partial_content'] = template.render(Context(partial_context))
        builder = generate_html(full_tree, appliers)
        context = build_context(context, builder)
        return context
