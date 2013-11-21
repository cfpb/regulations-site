#vim: set encoding=utf-8
from collections import defaultdict

from django.core.urlresolvers import reverse, NoReverseMatch
from django.http import HttpResponseBadRequest
from django.template import Context, loader
from django.views.generic.base import TemplateView

from regulations.generator import api_reader, generator, notices
from regulations.generator.layers.utils import convert_to_python
from regulations.generator.node_types import label_to_text
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

    def get_section(self, label):
        """ Get the section that the user came from. Special handling for
        an Interpretation section. """
        label = label.split('-')
        if 'Interp' in label:
            return '-'.join([label[0], 'Interp'])
        else:
            return '-'.join(label[:2])

    def get(self, request, *args, **kwargs):
        """Override this method so that we can grab the GET variables"""
        try:
            section_id = self.get_section(kwargs['label_id'])
            back_url = reverse('chrome_section_view', kwargs={
                'label_id': section_id,
                'version': request.GET.get('from_version')
            }) + '#' + kwargs['label_id']
            kwargs['back_url'] = back_url
            kwargs['version'] = request.GET.get('from_version')
            return super(ParagraphSXSView, self).get(request, *args,
                                                     **kwargs)
        except NoReverseMatch:
            return HttpResponseBadRequest("invalid from_version")

    def further_analyses(self, label_id, notice_id, version):
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
                    if a['reference'] != [notice_id, label_id]]

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
        notice_id = context['notice_id']

        notice = generator.get_notice(notice_id)
        if not notice:
            raise error_handling.MissingContentException()
        notice = convert_to_python(notice)

        paragraph_sxs = generator.get_sxs(label_id, notice)

        if paragraph_sxs is None:
            raise error_handling.MissingContentException()

        notices.add_depths(paragraph_sxs, 3)

        paragraph_sxs['children'] =\
            notices.filter_labeled_children(paragraph_sxs)
        self.footnote_refs(paragraph_sxs)

        context['sxs'] = paragraph_sxs
        context['sxs']['header'] = label_to_text(label_id.split('-'),
                                                 include_marker=True)
        context['sxs']['all_footnotes'] = self.footnotes(notice, paragraph_sxs)
        context['notice'] = notice
        context['further_analyses'] = self.further_analyses(
            label_id, notice_id, context['version'])

        return context
