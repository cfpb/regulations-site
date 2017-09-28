#vim: set encoding=utf-8
from collections import defaultdict

from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest
from django.http import Http404
from django.template import Context, loader
from django.views.generic.base import TemplateView

from regulations.generator import api_reader, generator, notices
from regulations.generator.layers.utils import convert_to_python
from regulations.generator.node_types import label_to_text
from regulations.generator.section_url import SectionUrl
from regulations.views import error_handling


class ParagraphSXSView(TemplateView):
    """ Given a regulation paragraph and a Federal Register notice number,
    display the appropriate section by section analyses."""
    def __init__(self):
        self.footnote_tpl = loader.get_template(
            "regulations/layers/sxs-footnotes.html")

    def get_template_names(self):
        """ The disclaimer that exists on this page can be over ridden. If an
        agency specfic disclaimer is provided, use that. """

        return ['regulations/sxs_with_disclaimer.html',
                'regulations/paragraph-sxs.html']

    def get(self, request, *args, **kwargs):
        """Override this method so that we can grab the GET variables
        and properly handle any errors."""
        kwargs['version'] = request.GET.get('from_version')
        kwargs['back_url'] = SectionUrl.of(
            kwargs['label_id'].split('-'), kwargs['version'], sectional=True)
        kwargs['fr_page'] = request.GET.get('fr_page')
        if kwargs['fr_page'] and kwargs['fr_page'].isdigit():
            kwargs['fr_page'] = int(kwargs['fr_page'])

        try:
            return super(ParagraphSXSView, self).get(request, *args, **kwargs)
        except error_handling.MissingContentException as e:
            raise Http404

    def further_analyses(self, label_id, notice_id, version,
            fr_page=None):
        """Grab other analyses for this same paragraph (limiting to those
           visible from this regulation version.) Make them in descending
           order"""
        sxs_layer_data = api_reader.ApiReader().layer('analyses', label_id,
                                                      version)

        if label_id not in sxs_layer_data:
            return []
        else:
            return [convert_to_python(a)
                    for a in reversed(sxs_layer_data[label_id])
                    if (a['reference'] != [notice_id, label_id]
                        or a.get('fr_page') != fr_page)]

    def footnote_refs(self, sxs):
        """Add footnote references to paragraph text"""
        refs = sxs.get('footnote_refs', [])
        ref_dict = defaultdict(list)
        for ref in refs:
            ref_dict[ref['paragraph']].append(ref)

        for p_idx in range(len(sxs['paragraphs'])):
            shift = 0
            for ref in ref_dict[p_idx]:
                p = sxs['paragraphs'][p_idx]
                rendered = self.footnote_tpl.render(Context({'footnote': ref}))
                offset = ref['offset'] + shift
                sxs['paragraphs'][p_idx] = p[:offset] + rendered
                sxs['paragraphs'][p_idx] += p[offset:]
                shift += len(rendered)
        for child in sxs['children']:
            self.footnote_refs(child)

    def footnotes(self, notice, sxs):
        """Data for footnotes (which are referenced in the paragraph text)"""
        feet = []
        for ref in sxs.get('footnote_refs', []):
            ref['text'] = notice['footnotes'][ref['reference']]
            feet.append(ref)
        for child in sxs['children']:
            feet = feet + self.footnotes(notice, child)
        return feet

    def get_context_data(self, **kwargs):
        context = super(ParagraphSXSView, self).get_context_data(**kwargs)

        label_id = context['label_id']
        part = label_id.split('-')[0]
        notice_id = context['notice_id']
        fr_page = context.get('fr_page')
        version = context.get('version', notice_id)

        # Try first to get the notice and SxS with the version.
        try:
            notice, paragraph_sxs = generator.get_notice_and_sxs(part, version,
                    label_id, fr_page)
        except TypeError:
            raise Http404

        if notice is None or paragraph_sxs is None:
            # If that didn't work, try again with the notice_id
            notice, paragraph_sxs = generator.get_notice_and_sxs(part,
                    notice_id, label_id, fr_page)
            if notice is None or paragraph_sxs is None:
                raise error_handling.MissingContentException()

        notices.add_depths(paragraph_sxs, 3)

        paragraph_sxs['children'] =\
            notices.filter_labeled_children(paragraph_sxs)
        self.footnote_refs(paragraph_sxs)

        context['sxs'] = paragraph_sxs
        # Template assumes a single label
        context['sxs']['label'] = context['label_id']
        context['sxs']['header'] = label_to_text(label_id.split('-'),
                                                 include_marker=True)
        context['sxs']['all_footnotes'] = self.footnotes(notice, paragraph_sxs)
        context['notice'] = notice
        context['further_analyses'] = self.further_analyses(
            label_id, notice_id, context['version'], paragraph_sxs.get('page'))

        return context
