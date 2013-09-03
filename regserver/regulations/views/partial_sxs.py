#vim: set encoding=utf-8
from django.core.urlresolvers import reverse, NoReverseMatch
from django.http import Http404, HttpResponseBadRequest
from django.views.generic.base import TemplateView

from regulations.generator import generator, notices
from regulations.generator.node_types import label_to_text


class ParagraphSXSView(TemplateView):
    """ Given a regulation paragraph and a Federal Register notice number,
    display the appropriate section by section analyses."""
    template_name = 'paragraph-sxs.html'

    def get(self, request, *args, **kwargs):
        """Override this method so that we can grab the GET variables"""
        try:
            label = kwargs['label_id'].split('-')
            section_id = '-'.join(label[:2])
            back_url = reverse('chrome_section_view', kwargs={
                'label_id': section_id,
                'version': request.GET.get('from_version')
            }) + '#' + kwargs['label_id']
            kwargs['back_url'] = back_url
            return super(ParagraphSXSView, self).get(request, *args,
                                                     **kwargs)
        except NoReverseMatch:
            return HttpResponseBadRequest("invalid from_version")

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
        context['sxs']['header'] = label_to_text(label_id.split('-'))

        return context
