#vim: set encoding=utf-8
from django.views.generic.base import TemplateView
from django.http import Http404

from regulations.generator import generator
from regulations.generator import notices


class ParagraphSXSView(TemplateView):
    """ Given a regulation paragraph and a Federal Register notice number,
    display the appropriate section by section analyses."""
    template_name = 'paragraph-sxs.html'

    def get_context_data(self, **kwargs):
        context = super(ParagraphSXSView, self).get_context_data(**kwargs)

        label_id = context['label_id']
        notice_id = context['notice_id']

        paragraph_sxs = generator.get_sxs(label_id, notice_id)

        if paragraph_sxs is None:
            raise Http404

        notices.add_depths(paragraph_sxs, 3)

        paragraph_sxs['children'] =\
            notices.filter_labeled_children(paragraph_sxs)
        context['sxs'] = paragraph_sxs

        return context
