from django.conf import settings
from django.views.generic.base import TemplateView
from django.template import Context, loader

from regulations.generator import generator
from regulations.generator.html_builder import HTMLBuilder
from regulations.views import utils
from regulations.views.partial import *


class ChromeView(TemplateView):
    """ Base class for views which wish to include chrome. """
    template_name = 'chrome.html'

    def add_extras(self, context):
        context['env'] = 'source' if settings.DEBUG else 'built'
        context['GOOGLE_ANALYTICS_SITE'] = settings.GOOGLE_ANALYTICS_SITE
        context['GOOGLE_ANALYTICS_ID'] = settings.GOOGLE_ANALYTICS_ID
        return context

    def get_context_data(self, **kwargs):
        context = super(ChromeView, self).get_context_data(**kwargs)

        label_id = context['label_id']
        version = context['version']

        if 'layers' in self.request.GET.keys():
            layer_names = self.request.GET['layers']
            appliers = utils.handle_specified_layers(layer_names, 
                        label_id, version)
        else:
            appliers = generator.get_all_layers(label_id, version)

        #   Hack solution: pull in full regulation, then the partial
        #   @todo: just query the meta and toc layers
        full_tree = generator.get_regulation(label_id.split('-')[0],
                version)
        relevant_tree = generator.get_tree_paragraph(label_id, version)
        
        partial_view = self.partial_class()
        partial_view.request = self.request
        partial_context = partial_view.get_context_data(label_id=label_id,
                version=version)
        template = loader.get_template(self.partial_class.template_name)

        context['partial_content'] = template.render(Context(partial_context))
        builder = generate_html(full_tree, appliers)

        context['tree'] = full_tree
        self.add_extras(context)

        return context


class ChromeInterpView(ChromeView):
    """Interpretation of regtext section/paragraph or appendix with chrome"""
    partial_class = PartialInterpView


class ChromeSectionView(ChromeView):
    """Regtext section with chrome"""
    partial_class = PartialSectionView


class ChromeParagraphView(ChromeView):
    """Regtext paragraph with chrome"""
    partial_class = PartialParagraphView

class ChromeRegulationView(ChromeView):
    """Entire regulation with chrome"""
    partial_class = PartialRegulationView
