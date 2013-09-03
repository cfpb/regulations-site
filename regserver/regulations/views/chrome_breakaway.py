from regulations.views.chrome import ChromeView
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

        label_id = context['label_id']

        #   @todo: get the regulation letter as well

        context['partial_content'] = self.content(context)

        self.add_extras(context)
        return context


class ChromeSXSView(ChromeBreakawayView):
    """SXS content"""
    def content(self, context):
        partial_view = ParagraphSXSView.as_view()
        response = partial_view(self.request, label_id=context['label_id'],
                                notice_id=context['notice_id'])
        response.render()
        return response.content
