from django.http import HttpResponse

from regulations.generator import api_reader
from regulations.views import utils
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

        context['regulation'] = context['label_id'].split('-')[0]
        context['version'] = self.request.GET.get('from_version')
        meta = api_reader.ApiReader().layer(
            'meta', context['regulation'], context['version'])
        context['meta'] = meta[context['regulation']][0]

        content = self.content(context)
        if isinstance(content, HttpResponse):  # error occurred
            return content
        context['partial_content'] = self.content(context)

        utils.add_extras(context)
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
