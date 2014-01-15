from django.core.urlresolvers import reverse, NoReverseMatch

from regulations.generator.node_types import to_markup_id


class SectionUrl(object):
    def __init__(self):
        self.rev_cache = {}

    def fetch(self, citation, version, sectional):
        key = (tuple(citation), version, sectional)
        if key not in self.rev_cache:
            url = ''

            view_name = 'chrome_section_view'
            # Subterps, collections of interpretations of whole subparts, etc.
            if 'Interp' in citation and ('Subpart' in citation
                                         or 'Appendices' in citation):
                view_name = 'chrome_subterp_view'
                label = '-'.join(citation)
            elif 'Interp' in citation:
                label = citation[0] + '-Interp'
            else:
                label = '-'.join(citation[:2])

            if sectional:
                try:
                    url = reverse(view_name, args=(label, version))
                except NoReverseMatch:
                    #XXX We have some errors in our layers. Once those are fixed,
                    #we need to revisit this.
                    pass
            self.rev_cache[key] = url + '#' + '-'.join(to_markup_id(citation))
        return self.rev_cache[key]

    @staticmethod
    def of(citation, version, sectional):
        return SectionUrl().fetch(citation, version, sectional)
