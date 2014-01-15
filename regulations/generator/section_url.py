from itertools import takewhile

from django.core.urlresolvers import reverse, NoReverseMatch

from regulations.generator.node_types import to_markup_id
from regulations.generator.toc import fetch_toc


class SectionUrl(object):
    def __init__(self):
        self.rev_cache = {}
        self.toc_cache = {}

    def fetch(self, citation, version, sectional):
        key = (tuple(citation), version, sectional)
        if key not in self.rev_cache:
            url = ''

            if sectional:
                view_name = 'chrome_section_view'
                # Subterps, collections of interps of whole subparts, etc.
                if 'Interp' in citation and ('Subpart' in citation
                                             or 'Appendices' in citation):
                    view_name = 'chrome_subterp_view'
                    label = '-'.join(citation)
                elif 'Interp' in citation:
                    view_name = 'chrome_subterp_view'
                    label = self.interp(citation, version)
                else:
                    label = '-'.join(citation[:2])

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
            if el['index'] == prefix_section:   # in a section, no subpart
                return reg_part + '-Subpart-Interp'
            for sub in el.get('sub_toc', []):
                #   In a subpart
                if sub['index'] == prefix_section and el.get('is_subpart'):
                    return '-'.join(el['index'][:3] + ['Interp'])
                #   In a subterp
                if sub['index'] == prefix:
                    return '-'.join(prefix)
        # Couldn't find it; most likely in the appendix
        return reg_part + '-Appendices-Interp'

    @staticmethod
    def of(citation, version, sectional):
        return SectionUrl().fetch(citation, version, sectional)
