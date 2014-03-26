#vim: set encoding=utf-8
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic.base import TemplateView

from regulations.generator import generator
from regulations.generator.html_builder import HTMLBuilder
from regulations.generator.node_types import EMPTYPART, REGTEXT, label_to_text
from regulations.views import navigation, utils


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

    def determine_appliers(self, label_id, version):
        """Figure out which layers to apply by checking the GET args"""
        if 'layers' in self.request.GET.keys():
            return utils.handle_specified_layers(
                self.request.GET['layers'], label_id, version,
                self.__class__.sectional_links)
        else:
            layer_creator = generator.LayerCreator()
            layer_creator.add_layers(
                generator.LayerCreator.LAYERS.keys(),
                label_id, version, self.__class__.sectional_links)
            return layer_creator.get_appliers()

    def get_context_data(self, **kwargs):
        context = super(PartialView, self).get_context_data(**kwargs)

        label_id = context['label_id']
        version = context['version']

        tree = generator.get_tree_paragraph(label_id, version)
        if tree is None:
            raise Http404

        inline_applier, p_applier, s_applier = self.determine_appliers(
            label_id, version)

        builder = generate_html(tree, (inline_applier, p_applier, s_applier))
        return self.transform_context(context, builder)


class PartialSectionView(PartialView):
    """ Single section of reg text """
    template_name = 'regulations/regulation-content.html'

    def section_navigation(self, label, version):
        nav_sections = navigation.nav_sections(label, version)
        if nav_sections:
            p_sect, n_sect = nav_sections

            nav = {'previous': p_sect, 'next': n_sect}
            return nav

    def transform_context(self, context, builder):
        child_of_root = builder.tree
        #   Add a layer to account for subpart if this is regtext
        if builder.tree['node_type'] == REGTEXT:
            child_of_root = {
                'node_type': EMPTYPART,
                'children': [builder.tree]}
        context['markup_page_type'] = 'reg-section'
        context['tree'] = {'children': [child_of_root]}
        context['navigation'] = self.section_navigation(
            context['label_id'], context['version'])

        return context


class PartialParagraphView(PartialSectionView):
    """ Single paragraph of a regtext """
    def transform_context(self, context, builder):
        node = builder.tree
        # Wrap with layers until we reach a section
        while len(node['label']) > 2:
            node = {'node_type': node['node_type'],
                    'children': [node],
                    'label': node['label'][:-1]}

        # added to give the proper parent container ID
        # when interp headers are rendered
        node['markup_id'] = context['label_id']

        # One more layer for regtext
        if node['node_type'] == REGTEXT:
            node = {'node_type': EMPTYPART,
                    'children': [node],
                    'label': node['label'][:1] + ['Subpart']}

        context['markup_page_type'] = 'reg-section'
        context['tree'] = {'children': [node], 'label': node['label'][:1],
                           'node_type': REGTEXT}
        context['navigation'] = self.section_navigation(
            context['label_id'], context['version'])
        return context


class PartialDefinitionView(PartialView):
    """ Single paragraph of a regtext formatted for display
        as an inline interpretation """

    template_name = "regulations/partial-definition.html"

    def transform_context(self, context, builder):
        context['node'] = builder.tree
        context['formatted_label'] = label_to_text(
            builder.tree['label'], True, True)
        context['node']['section_id'] = '%s-%s' % (
            builder.tree['label'][0], builder.tree['label'][1])
        return context


class PartialRegulationView(PartialView):
    """ Entire regulation without chrome """

    template_name = 'regulations/regulation-content.html'
    sectional_links = False

    def transform_context(self, context, builder):
        context['tree'] = builder.tree
        return context
