#vim: set encoding=utf-8
from django.views.generic.base import TemplateView
from django.http import Http404

from regulations.generator import generator
from regulations.generator.html_builder import HTMLBuilder
from regulations.generator.node_types import EMPTYPART, REGTEXT
from regulations.views import utils
from regulations.generator import navigation


def generate_html(regulation_tree, layer_appliers):
    builder = HTMLBuilder(*layer_appliers)
    builder.tree = regulation_tree
    builder.generate_html()
    return builder


class PartialView(TemplateView):
    """Base class of various partial markup views. sectional_links indicates
    whether this view should use section links (url to a path) or just hash
    links (to an anchor on the page)"""

    sectional_links = True

    def get_context_data(self, **kwargs):
        context = super(PartialView, self).get_context_data(**kwargs)

        label_id = context['label_id']
        version = context['version']

        tree = generator.get_tree_paragraph(label_id, version)
        if tree is None:
            raise Http404

        if 'layers' in self.request.GET.keys():
            appliers = utils.handle_specified_layers(
                self.request.GET['layers'],
                label_id, version, self.__class__.sectional_links)
            inline_applier, p_applier, s_applier = appliers
        else:
            layer_creator = generator.LayerCreator()
            layer_creator.add_layers(
                generator.LayerCreator.LAYERS.keys(),
                label_id, version, self.__class__.sectional_links)
            inline_applier, p_applier, s_applier = layer_creator.get_appliers()

        
        builder = generate_html(tree, (inline_applier, p_applier, s_applier))
        return self.transform_context(context, builder)


class PartialSectionView(PartialView):
    """ Single section of reg text """
    template_name = 'regulation-content.html'

    def section_navigation(self, label, version):
        nav_sections = navigation.nav_sections(label, version)
        if nav_sections:
            p_sect, n_sect = nav_sections

            nav = {}
            if p_sect:
                nav['previous'] = navigation.parse_section_title(p_sect)
            if n_sect:
                nav['next'] = navigation.parse_section_title(n_sect)
            return nav

    def transform_context(self, context, builder):
        child_of_root = builder.tree
        #   Add a layer to account for subpart if this is regtext
        if builder.tree['node_type'] == REGTEXT:
            child_of_root = {
                'node_type': EMPTYPART,
                'children': [builder.tree]}
        context['tree'] = {'children': [child_of_root]}
        context['navigation'] = self.section_navigation(
            context['label_id'], context['version'])

        return context


class PartialParagraphView(PartialView):
    """ Single paragraph of a regtext """

    template_name = "tree.html"

    def transform_context(self, context, builder):
        context['node'] = builder.tree
        return context


class PartialInterpView(PartialView):
    """ Interpretation of a reg text section/paragraph or appendix """

    template_name = "interpretations.html"
    inline = False

    def transform_context(self, context, builder):
        context['inline'] = self.inline
        context['c'] = {'node_type': 'interp', 'children': [builder.tree]}
        return context


class PartialRegulationView(PartialView):
    """ Entire regulation without chrome """

    template_name = 'regulation-content.html'
    sectional_links = False

    def transform_context(self, context, builder):
        context['tree'] = builder.tree
        return context
