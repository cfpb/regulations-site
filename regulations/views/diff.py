#vim: set encoding=utf-8

from regulations.generator import generator
from regulations.generator.html_builder import HTMLBuilder
from regulations.generator.layers.toc_applier import TableOfContentsLayer
from regulations.generator.node_types import EMPTYPART, REGTEXT
from regulations.generator.section_url import SectionUrl
from regulations.generator.toc import fetch_toc
from regulations.views import error_handling, utils
from regulations.views.chrome import ChromeView
from regulations.views.navigation import choose_next_section
from regulations.views.navigation import choose_previous_section
from regulations.views.partial import PartialView

from django.core.urlresolvers import reverse


def get_appliers(label_id, older, newer):
    diff = generator.get_diff_applier(label_id, older, newer)

    if diff is None:
        raise error_handling.MissingContentException()

    appliers = utils.handle_diff_layers(
        'graphics,paragraph,keyterms,defined',
        label_id,
        older,
        newer)
    appliers += (diff,)
    return appliers


class PartialSectionDiffView(PartialView):
    """ A diff view of a partial section. """
    template_name = 'regulations/regulation-content.html'

    def get(self, request, *args, **kwargs):
        """ Override GET so that we can catch and propagate any errors. """

        try:
            return super(PartialSectionDiffView, self).get(request, *args,
                                                           **kwargs)
        except error_handling.MissingContentException, e:
            return error_handling.handle_generic_404(request)

    def footer_nav(self, label, toc, old_version, new_version, from_version):
        nav = {}
        for idx, toc_entry in enumerate(toc):
            if toc_entry['section_id'] != label:
                continue

            p_sect = choose_previous_section(idx, toc)
            n_sect = choose_next_section(idx, toc)

            if p_sect:
                nav['previous'] = p_sect
                nav['previous']['url'] = reverse_chrome_diff_view(
                    p_sect['section_id'], old_version,
                    new_version, from_version)

            if n_sect:
                nav['next'] = n_sect
                nav['next']['url'] = reverse_chrome_diff_view(
                    n_sect['section_id'], old_version,
                    new_version, from_version)
        return nav

    def get_context_data(self, **kwargs):
        # We don't want to run the content data of PartialView -- it assumes
        # we will be applying layers
        context = super(PartialView, self).get_context_data(**kwargs)

        label_id = context['label_id']
        older = context['version']
        newer = context['newer_version']

        tree = generator.get_tree_paragraph(label_id, older)

        if tree is None:
            #TODO We need a more complicated check here to see if the diffs
            #add the requested section. If not -> 404
            tree = {}

        appliers = get_appliers(label_id, older, newer)

        builder = HTMLBuilder(*appliers)
        builder.tree = tree

        if not builder.tree:
            return error_handling.handle_generic_404(self.request)

        builder.generate_html()

        child_of_root = builder.tree
        if builder.tree['node_type'] == REGTEXT:
            child_of_root = {
                'node_type': EMPTYPART,
                'children': [builder.tree]}
        context['tree'] = {'children': [child_of_root]}
        context['markup_page_type'] = 'diff'

        regpart = label_id.split('-')[0]
        old_toc = fetch_toc(regpart, older)
        diff = generator.get_diff_json(regpart, older, newer)
        from_version = self.request.GET.get('from_version', older)
        context['TOC'] = diff_toc(older, newer, old_toc, diff, from_version)
        context['navigation'] = self.footer_nav(label_id, context['TOC'],
                                                older, newer, from_version)
        return context


class ChromeSectionDiffView(ChromeView):
    """Search results with chrome"""
    template_name = 'regulations/diff-chrome.html'
    partial_class = PartialSectionDiffView
    has_sidebar = False

    def check_tree(self, context):
        pass    # The tree may or may not exist in the particular version

    def add_diff_content(self, context):
        context['from_version'] = self.request.GET.get(
            'from_version', context['version'])
        context['left_version'] = context['version']
        context['right_version'] = \
            context['main_content_context']['newer_version']
        from_version = self.request.GET.get('from_version', context['version'])

        context['TOC'] = context['main_content_context']['TOC']

        #   Add reference to the first subterp, so we know how to redirect
        toc = fetch_toc(context['label_id'].split('-')[0], from_version)
        for entry in toc:
            if entry.get('is_supplement') and entry.get('sub_toc'):
                el = entry['sub_toc'][0]
                el['url'] = SectionUrl().of(
                    el['index'], from_version,
                    self.partial_class.sectional_links)
                context['first_subterp'] = el
        return context

    def add_main_content(self, context):
        super(ChromeSectionDiffView, self).add_main_content(context)
        return self.add_diff_content(context)


def reverse_chrome_diff_view(sect_id, left_ver, right_ver, from_version):
    """ Reverse the URL for a chromed diff view. """

    diff_url = reverse(
        'chrome_section_diff_view',
        args=(sect_id, left_ver, right_ver))
    diff_url += '?from_version=%s' % from_version
    return diff_url


def extract_sections(toc):
    compiled_toc = []
    for i in toc:
        if 'Subpart' in i['index']:
            compiled_toc.extend(i['sub_toc'])
        else:
            compiled_toc.append(i)
    return compiled_toc


def diff_toc(older_version, newer_version, old_toc, diff, from_version):
    #We work around Subparts in the TOC for now.
    compiled_toc = extract_sections(old_toc)

    for node in (v['node'] for v in diff.values() if v['op'] == 'added'):
        if len(node['label']) == 2 and node['title']:
            element = {
                'label': node['title'],
                'index': node['label'],
                'section_id': '-'.join(node['label']),
                'op': 'added'
            }
            data = {'index': node['label'], 'title': node['title']}
            TableOfContentsLayer.section(element, data)
            TableOfContentsLayer.appendix_supplement(element, data)
            compiled_toc.append(element)

    modified, deleted = modified_deleted_sections(diff)
    for el in compiled_toc:
        if not 'Subpart' in el['index']:
            el['url'] = reverse_chrome_diff_view(
                el['section_id'], older_version, newer_version, from_version)
        # Deleted first, lest deletions in paragraphs affect the section
        if tuple(el['index']) in deleted and 'op' not in el:
            el['op'] = 'deleted'
        if tuple(el['index']) in modified and 'op' not in el:
            el['op'] = 'modified'

    return sort_toc(compiled_toc)


def sort_toc(toc):
    """ Sort the Table of Contents elements. """

    def normalize(element):
        """ Return a sorting order for a TOC element, primarily based
        on the index, and the type of content. """

        # The general order of a regulation is: regulation text sections,
        # appendices, and then the interpretations.

        normalized = []
        if element.get('is_section'):
            normalized.append(0)
        elif element.get('is_appendix'):
            normalized.append(1)
        elif element.get('is_supplement'):
            normalized.append(2)

        for part in element['index']:
            if part.isdigit():
                normalized.append(int(part))
            else:
                normalized.append(part)
        return normalized

    return sorted(toc, key=lambda el: tuple(normalize(el)))


def modified_deleted_sections(diff):
    modified, deleted = set(), set()
    for label, diff_value in diff.iteritems():
        label = tuple(label.split('-'))
        if 'Interp' in label:
            section_label = (label[0], 'Interp')
        else:
            section_label = tuple(label[:2])

        # Whole section was deleted
        if diff_value['op'] == 'deleted' and label == section_label:
            deleted.add(section_label)
        # Whole section added/modified or paragraph added/deleted/modified
        else:
            modified.add(section_label)
    return modified, deleted
