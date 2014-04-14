from itertools import takewhile

from django.core.urlresolvers import reverse, NoReverseMatch

from regulations.generator.node_types import to_markup_id
from regulations.generator.toc import fetch_toc


class SectionUrl(object):
    """With few exceptions, users are expected to browse the regulation by
    traversing regtext sections, appendices, and subterps (split
    interpretations). This object will deduce, from a version and citation,
    to which section/appendix/subterp to link, a task greatly complicated by
    subterps. Importantly, this object keeps a cache of looked up info;
    reusing an instance is significantly faster than using static methods."""
    def __init__(self):
        self.rev_cache = {}
        self.toc_cache = {}

    def view_label_id(self, citation, version):
        # Subterps, collections of interps of whole subparts, etc.
        if 'Interp' in citation and ('Subpart' in citation
                                     or 'Appendices' in citation):
            label = '-'.join(citation)
        elif 'Interp' in citation:
            label = self.interp(citation, version)
        else:
            label = '-'.join(citation[:2])
        return label

    def fetch(self, citation, version, sectional):
        key = (tuple(citation), version, sectional)
        if key not in self.rev_cache:
            url = ''

            if sectional:
                view_name = 'chrome_section_view'
                if len(citation) > 1 and citation[1] == 'Interp':
                    view_name = 'chrome_paragraph_view'
                elif 'Interp' in citation:
                    view_name = 'chrome_subterp_view'
                label = self.view_label_id(citation, version)

                try:
                    url = reverse(view_name, args=(label, version))
                except NoReverseMatch:
                    #XXX We have some errors in our layers. Once those are
                    # fixed, we need to revisit this.
                    pass
            self.rev_cache[key] = url + '#' + '-'.join(to_markup_id(citation))
        return self.rev_cache[key]

    def interp(self, citation, version):
        """Subterps throw a big monkey-wrench into things. Citations to
        interpretations must be converted into their corresponding subterp,
        which requires loading the toc."""
        reg_part = citation[0]
        key = (reg_part, version)
        prefix = list(takewhile(lambda l: l != 'Interp', citation))
        prefix.append('Interp')
        if key not in self.toc_cache:
            self.toc_cache[key] = fetch_toc(reg_part, version)

        prefix_section = prefix[:2]
        for el in self.toc_cache[key]:
            if el['index'] == prefix_section and el.get('is_section'):
                # No subpart
                return reg_part + '-Subpart-Interp'
            for sub in el.get('sub_toc', []):
                #   In a subpart
                if sub['index'] == prefix_section and el.get('is_subpart'):
                    return '-'.join(el['index'][:3] + ['Interp'])
                #   In a subterp
                if sub['index'] == prefix:
                    return '-'.join(prefix)
                #   Other match: interpretation header
                if sub['index'] == citation[:len(sub['index'])]:
                    return sub['section_id']
        # Couldn't find it; most likely in the appendix
        return reg_part + '-Appendices-Interp'

    @staticmethod
    def of(citation, version, sectional):
        return SectionUrl().fetch(citation, version, sectional)
