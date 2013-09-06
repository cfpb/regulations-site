from django.conf import settings
from django.http import HttpResponseBadRequest
from django.views.generic.base import TemplateView

from regulations.generator import api_reader
from regulations.generator.node_types import label_to_text
from regulations.generator.versions import fetch_grouped_history


API_PAGE_SIZE = 50
PAGE_SIZE = 10


class PartialSearch(TemplateView):
    """Display search results without any chrome."""
    template_name = 'search-results.html'

    def get(self, request, *args, **kwargs):
        """Override this method so we can return a 400 if needed"""
        query = request.GET.get('q')
        version = request.GET.get('version')
        if not query or not version:
            return HttpResponseBadRequest("missing query or version")

        kwargs['q'] = query
        kwargs['version'] = version
        return super(PartialSearch, self).get(request, *args, **kwargs)

    def add_prev_next(self, current_page, context):
        if current_page > 0:
            context['previous'] = {'length': PAGE_SIZE,
                                   'page': current_page - 1}
        max_this_page = (current_page + 1) * PAGE_SIZE
        remaining = context['results']['total_hits'] - max_this_page
        if remaining > 0:
            context['next'] = {'page': current_page + 1,
                               'length': min(remaining, PAGE_SIZE)}

    def get_context_data(self, **kwargs):
        context = super(PartialSearch, self).get_context_data(**kwargs)

        try:
            page = int(self.request.GET.get('page', '0'))
        except ValueError:
            page = 0

        # API page size is API_PAGE_SIZE, but we show only PAGE_SIZE
        api_page = page // (API_PAGE_SIZE/PAGE_SIZE)
        page_idx = (page % (API_PAGE_SIZE/PAGE_SIZE)) * PAGE_SIZE

        results = api_reader.ApiReader().search(
            context['q'], context['version'], context['label_id'], api_page)

        # Ignore results found in the root (i.e. not a section)
        results['results'] = [r for r in results['results']
                              if len(r['label']) > 1]
        results['results'] = results['results'][page_idx:page_idx + PAGE_SIZE]

        for result in results['results']:
            result['header'] = label_to_text(result['label'])
            if 'Interp' in result['label']:
                result['section_id'] = '%s-%s' % (result['label'][0],
                                                  'Interp')
            else:
                result['section_id'] = '-'.join(result['label'][:2])
        context['results'] = results

        for version in fetch_grouped_history(context['label_id']):
            for notice in version['notices']:
                if notice['document_number'] == context['version']:
                    context['version_by_date'] = notice['effective_on']
                    context['version_timeline'] = version['timeline']

        self.add_prev_next(page, context)

        return context
