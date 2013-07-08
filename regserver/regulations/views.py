
from django.conf import settings
from django.views.generic.base import TemplateView
from regulations.generator import generator
from regulations.generator.html_builder import HTMLBuilder

class RegulationView(TemplateView):
    template_name = "simpler.html"

    @staticmethod
    def get_regulation_part(reg_part_section):
        if '-' in reg_part_section:
            return reg_part_section.split('-')[0]
        else:
            return reg_part_section

    def get_context_data(self, **kwargs):
        context = super(RegulationView, self).get_context_data(**kwargs)
        #context['message'] = 'regulation %s | version %s'  % (context['reg_part_section'], context['reg_version'])

        regulation_part = context['reg_part_section']
        regulation_version = context['reg_version']

        regulation = RegulationView.get_regulation_part(context['reg_part_section'])
        inline_applier, p_applier, s_applier = generator.get_all_layers(regulation_part, regulation_version)

        p_applier = generator.add_full_toc(regulation, regulation_version, p_applier)
        section_tree = generator.get_regulation_section(regulation, 
                            regulation_version, context['reg_part_section'])

        builder = HTMLBuilder(inline_applier, p_applier, s_applier)
        builder.tree = section_tree

        builder.generate_html()

        context['tree'] = builder.tree
        context['env'] = builder.get_env_dir()
        context['GOOGLE_ANALYTICS_SITE'] = settings.GOOGLE_ANALYTICS_SITE
        context['GOOGLE_ANALYTICS_ID'] = settings.GOOGLE_ANALYTICS_ID

        return context
