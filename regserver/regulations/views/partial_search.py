from django.conf import settings
from django.http import HttpResponseBadRequest
from django.views.generic.base import TemplateView

from regulations.generator import api_reader
from regulations.generator.node_types import label_to_text


class PartialSearch(TemplateView):
    """Display search results without any chrome."""
    template_name = 'search-results.html'

    def get(self, request, *args, **kwargs):
        """Override this method so that we can grab the GET variables"""
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

        for result in results['results']:
            result['header'] = label_to_text(result['label'])
            if 'Interp' in result['label']:
                result['section_id'] = '%s-%s' % (result['label'][0],
                                                  'Interp')
            else:
                result['section_id'] = '-'.join(result['label'][:2])
        context['results'] = results

        return context
