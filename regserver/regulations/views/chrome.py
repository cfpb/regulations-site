from datetime import date

from django.conf import settings
from django.views.generic.base import TemplateView

from regulations.generator import generator
from regulations.generator.versions import fetch_grouped_history
from regulations.views import utils
from regulations.views.diff import PartialSectionDiffView
from regulations.views.landing import regulation_exists, get_versions, regulation as landing_page
from regulations.views.partial import *
from regulations.views.partial_search import PartialSearch
from regulations.views.sidebar import SideBarView
from regulations.views import error_handling


class ChromeView(TemplateView):
    """ Base class for views which wish to include chrome. """
    template_name = 'chrome.html'
    has_sidebar = True

    def get(self, request, *args, **kwargs):
        """Override GET so that we can catch and propagate any errors in the
        included partial(s)"""

        try:
            return super(ChromeView, self).get(request, *args, **kwargs)
        except BadComponentException, e:
            return e.response
        except error_handling.MissingSectionException, e:
            return error_handling.handle_missing_section_404(
                request, e.label_id, e.version, e.context)
        except error_handling.MissingContentException, e:
            return error_handling.handle_generic_404(request)

    def _assert_good(self, response):
        if response.status_code != 200:
            raise BadComponentException(response)

    def process_partial(self, context):
        partial_view = self.partial_class.as_view()
        response = partial_view(self.request,
                                label_id=context['label_id'],
                                version=context['version'])
        self._assert_good(response)
        response.render()
        return response.content

    def set_tree_context(self, context, label_id, version):
        #   Hack solution: pull in full regulation, then the partial
        #   @todo: just query the meta and toc layers
        part = label_id.split('-')[0]
        full_tree = generator.get_regulation(part, version)

        if full_tree is None:
            raise error_handling.MissingContentException()
        
        appliers = utils.handle_specified_layers(
            'toc,meta', part, version, self.partial_class.sectional_links)
        builder = generate_html(full_tree, appliers)

        context['tree'] = full_tree
        utils.add_extras(context)

        context['part'] = part
        context['history'] = fetch_grouped_history(part)

        context['today'] = date.today()

    def get_context_data(self, **kwargs):

        context = super(ChromeView, self).get_context_data(**kwargs)

        label_id = context['label_id']
        version = context['version']

        self.set_tree_context(context, label_id, version)
       
        relevant_tree = generator.get_tree_paragraph(label_id, version)
        if relevant_tree is None:
            raise error_handling.MissingSectionException(label_id, version, context)

        context['partial_content'] = self.process_partial(context)
        if self.has_sidebar:
            sidebar_view = SideBarView.as_view()
            response = sidebar_view(self.request, label_id=label_id,
                                    version=version)
            self._assert_good(response)
            response.render()
            context['sidebar_content'] = response.content


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


class ChromeSearchView(ChromeView):
    """Search results with chrome"""
    template_name = 'chrome-empty-sidebar.html'
    partial_class = PartialSearch
    has_sidebar = False

    def get_context_data(self, **kwargs):
        """Get the version and label_id for the chrome context"""
        kwargs['version'] = self.request.GET.get('version', '')
        # Use the first section for the chrome -- does not work in all regs
        kwargs['label_id'] = kwargs['label_id'] + '-1'
        return super(ChromeSearchView, self).get_context_data(**kwargs)


class ChromeSectionDiffView(ChromeView):
    """Search results with chrome"""
    partial_class = PartialSectionDiffView

    def process_partial(self, context):
        """Must override the parameters to this partial as it needs to have
        a 'newer_version' field"""
        partial_view = self.partial_class.as_view()
        response = partial_view(self.request,
                                label_id=context['label_id'],
                                version=context['version'],
                                newer_version=context['newer_version'])
        self._assert_good(response)
        response.render()
        return response.content


class ChromeLandingView(ChromeView):
    """Landing page with chrome"""
    template_name = 'landing-chrome.html'
    partial_class = PartialSectionView  # Needed to know sectional status
    has_sidebar = False

    def process_partial(self, context):
        """Landing page isn't a TemplateView"""
        response = landing_page(self.request, context['regulation'])
        self._assert_good(response)
        return response.content

    def get_context_data(self, **kwargs):
        """Add the version and replace the label_id for the chrome context"""

        if not regulation_exists(kwargs['label_id']):
            raise error_handling.MissingContentException()

        current, _ = get_versions(kwargs['label_id'])
        kwargs['version'] = current['version']
        kwargs['regulation'] = kwargs['label_id']
        # Use the first section for the chrome -- does not work in all regs
        kwargs['label_id'] = kwargs['label_id'] + '-1'
        return super(ChromeLandingView, self).get_context_data(**kwargs)


class BadComponentException(Exception):
    """Allows us to propagate errors in loaded partials"""
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "BadComponentException(response=%s)" % repr(self.response)
