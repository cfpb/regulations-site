from django.views.generic.base import TemplateView

from regulations.generator import api_reader
from regulations.generator.layers.analyses import SectionBySectionLayer


class SideBarView(TemplateView):
    """ View for handling the right-side sidebar """
    template_name = 'sidebar.html'

    def get_context_data(self, **kwargs):
        context = super(SideBarView, self).get_context_data(**kwargs)

        label_id = context['label_id']
        version = context['version']

        client = api_reader.ApiReader()
        sxs_layer_data = client.layer('analyses', label_id, version)
        sxs_layer = SectionBySectionLayer(sxs_layer_data)
        result = sxs_layer.apply_layer(label_id)
        if result:
            context[result[0]] = result[1]

        return context
