from django.conf import settings
from django.views.generic.base import TemplateView

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

        #   Hack solution: pull in full regulation, then the partial
        #   @todo: just query the meta and toc layers
        part = label_id.split('-')[0]
        full_tree = generator.get_regulation(part, version)
        relevant_tree = generator.get_tree_paragraph(label_id, version)
        
        partial_view = self.partial_class.as_view()
        response = partial_view(self.request, label_id=label_id,
                version=version)
        response.render()
        context['partial_content'] = response.content

        appliers = utils.handle_specified_layers('toc,meta', part, version)
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
