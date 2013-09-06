from django.conf import settings
from django.http import HttpResponseBadRequest
from django.views.generic.base import TemplateView

from regulations.generator import api_reader
from regulations.generator.node_types import label_to_text
from regulations.generator.versions import fetch_grouped_history


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

    def get_context_data(self, **kwargs):
        context = super(PartialSearch, self).get_context_data(**kwargs)

        results = api_reader.ApiReader().search(kwargs['q'], kwargs['version'])
        # Ignore results found in the root (i.e. not a section)
        results['results'] = [r for r in results['results']
                              if len(r['label']) > 1]

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
                if notice['document_number'] == kwargs['version']:
                    context['version_by_date'] = notice['effective_on']
                    context['version_timeline'] = version['timeline']

        return context
