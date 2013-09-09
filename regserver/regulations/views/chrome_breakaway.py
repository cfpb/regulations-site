from django.http import HttpResponse

from regulations.views.chrome import ChromeView
from regulations.views.partial_search import PartialSearch
from regulations.views.partial_sxs import ParagraphSXSView


class ChromeBreakawayView(ChromeView):
    """ Base class for views which wish to include chrome. """
    template_name = 'breakaway-chrome.html'

    def content(self, context):
        """Filled in by subclasses; content for the breakaway"""
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        #   Skip ChromeView's implementation
        context = super(ChromeView, self).get_context_data(**kwargs)

        #   @todo: get the regulation letter as well

        content = self.content(context)
        if isinstance(content, HttpResponse):  # error occurred
            return content
        context['partial_content'] = self.content(context)

        self.add_extras(context)
        return context


class ChromeSXSView(ChromeBreakawayView):
    """SXS content"""
    def content(self, context):
        partial_view = ParagraphSXSView.as_view()
        response = partial_view(self.request, label_id=context['label_id'],
                                notice_id=context['notice_id'])
        self._assert_good(response)
        response.render()
        return response.content


class ChromeSearchView(ChromeBreakawayView):
    """Search results"""
    def content(self, context):
        partial_view = PartialSearch.as_view()
        response = partial_view(self.request, label_id=context['label_id'])
        self._assert_good(response)
        response.render()
        return response.content
