import logging
import re

from django.conf import settings

import api_reader
from layers.defined import DefinedLayer
from layers.definitions import DefinitionsLayer
from layers.external_citation import ExternalCitationLayer
from layers.formatting import FormattingLayer
from layers.internal_citation import InternalCitationLayer
from layers.interpretations import InterpretationsLayer
from layers.key_terms import KeyTermsLayer
from layers.meta import MetaLayer
from layers.layers_applier import InlineLayersApplier
from layers.layers_applier import ParagraphLayersApplier
from layers.layers_applier import SearchReplaceLayersApplier
from layers.paragraph_markers import ParagraphMarkersLayer
from layers.toc_applier import TableOfContentsLayer
from layers.graphics import GraphicsLayer
from layers.diff_applier import DiffApplier
from layers.utils import convert_to_python
from html_builder import HTMLBuilder
import notices


class LayerCreator(object):
    """ This lets us dynamically load layers by shorthand. """
    DEFINED = DefinedLayer.shorthand
    EXTERNAL = ExternalCitationLayer.shorthand
    GRAPHICS = GraphicsLayer.shorthand
    INTERNAL = InternalCitationLayer.shorthand
    INTERP = InterpretationsLayer.shorthand
    KEY_TERMS = KeyTermsLayer.shorthand
    META = MetaLayer.shorthand
    PARAGRAPH = ParagraphMarkersLayer.shorthand
    FORMATTING = FormattingLayer.shorthand
    TERMS = DefinitionsLayer.shorthand
    TOC = TableOfContentsLayer.shorthand

    LAYERS = {
        DEFINED: ('terms', 'inline', DefinedLayer),
        #EXTERNAL: ('external-citations', 'inline', ExternalCitationLayer),
        GRAPHICS: ('graphics', 'search_replace', GraphicsLayer),
        INTERNAL: ('internal-citations', 'inline', InternalCitationLayer),
        INTERP: ('interpretations', 'paragraph', InterpretationsLayer),
        KEY_TERMS: ('keyterms', 'search_replace', KeyTermsLayer),
        META: ('meta', 'paragraph', MetaLayer),
        PARAGRAPH: (
            'paragraph-markers', 'search_replace', ParagraphMarkersLayer),
        FORMATTING: ('formatting', 'search_replace', FormattingLayer),
        TERMS: ('terms', 'inline', DefinitionsLayer),
        TOC: ('toc', 'paragraph', TableOfContentsLayer),
    }

    def __init__(self):
        self.appliers = {
            'inline': InlineLayersApplier(),
            'paragraph': ParagraphLayersApplier(),
            'search_replace': SearchReplaceLayersApplier()}

        self.api = api_reader.ApiReader()

    def get_layer_json(self, api_name, regulation, version):
        """ Hit the API to retrieve the regulation JSON. """
        return self.api.layer(api_name, regulation, version)

    def add_layer(self, layer_name, regulation, version, sectional=False):
        """ Add a normal layer (no special handling required) to the applier.
        """

        if layer_name.lower() in LayerCreator.LAYERS:
            api_name, applier_type,\
                layer_class = LayerCreator.LAYERS[layer_name]
            layer_json = self.get_layer_json(api_name, regulation, version)
            if layer_json is None:
                logging.warning("No data for %s/%s/%s"
                                % (api_name, regulation, version))
            else:
                layer = layer_class(layer_json)

                if sectional and hasattr(layer, 'sectional'):
                    layer.sectional = sectional
                if hasattr(layer, 'version'):
                    layer.version = version

                self.appliers[applier_type].add_layer(layer)

    def add_layers(self, layer_names, regulation, version, sectional=False):
        """Request a list of layers."""
        #This doesn't deal with sectional interpretations yet.
        #we'll have to do that.
        layer_names = set(filter(lambda l: l.lower() in LayerCreator.LAYERS,
                                 layer_names))
 
        #   Spawn threads
        for layer_name in layer_names:
            api_name, applier_type, layer_class = LayerCreator.LAYERS[layer_name]
            layer_json = self.get_layer_json(api_name, regulation, version)

            if layer_json is None:
                logging.warning("No data for %s/%s/%s"
                                % (api_name, regulation, version))
            else:
                layer = layer_class(layer_json)
 
                if sectional and hasattr(layer, 'sectional'):
                    layer.sectional = sectional
                if hasattr(layer, 'version'):
                    layer.version = version
 
                self.appliers[applier_type].add_layer(layer)

    def get_appliers(self):
        """ Return the appliers. """
        return (self.appliers['inline'],
                self.appliers['paragraph'],
                self.appliers['search_replace'])


class DiffLayerCreator(LayerCreator):
    def __init__(self, newer_version):
        super(DiffLayerCreator, self).__init__()
        self.newer_version = newer_version

    @staticmethod
    def combine_layer_versions(older_layer, newer_layer):
        """ Create a new layer by taking all the nodes from the older
        layer, and adding to the all the new nodes from the newer layer. """

        combined_layer = {}

        for n in older_layer:
            combined_layer[n] = older_layer[n]

        for n in newer_layer:
            if n not in combined_layer:
                combined_layer[n] = newer_layer[n]

        return combined_layer

    def get_layer_json(self, api_name, regulation, version):
        older_layer = self.api.layer(api_name, regulation, version)
        newer_layer = self.api.layer(api_name, regulation, self.newer_version)

        layer_json = self.combine_layer_versions(older_layer, newer_layer)
        return layer_json


def get_regulation(regulation, version):
    """ Get the regulation JSON tree. Manipulate the label a bit for easier
    access in the templates."""
    api = api_reader.ApiReader()
    reg = api.regulation(regulation, version)

    if reg:
        title = reg['title']
        # up till the paren
        match = re.search('part \d+[^\w]*([^\(]*)', title, re.I)
        if match:
            reg['title_clean'] = match.group(1).strip()
        match = re.search('\(regulation (\w+)\)', title, re.I)
        if match:
            reg['reg_letter'] = match.group(1)

        return reg


def get_tree_paragraph(paragraph_id, version):
    """Get a single level of the regulation tree."""
    api = api_reader.ApiReader()
    return api.regulation(paragraph_id, version)


def get_builder(regulation, version, inline_applier, p_applier, s_applier):
    """ Returns an HTML builder with the appliers, and the regulation tree. """
    builder = HTMLBuilder(inline_applier, p_applier, s_applier)
    builder.tree = get_regulation(regulation, version)
    return builder


def get_all_notices(part):
    api = api_reader.ApiReader()
    return notices.fetch_all(api, part)


def get_notice(part, document_number):
    """ Get a the data from a particular notice, given the Federal Register
    document number. """

    api = api_reader.ApiReader()
    return api.notice(part, document_number)


def get_sxs(label_id, notice, fr_page=None):
    """ Given a paragraph label_id, find the sxs analysis for that paragraph if
    it exists and has content. fr_page is used to distinguish between
    multiple analyses in the same notice."""

    all_sxs = notice['section_by_section']
    relevant_sxs = notices.find_label_in_sxs(all_sxs, label_id, fr_page)

    return relevant_sxs


def get_notice_and_sxs(part, notice_id, label_id, fr_page):
    """ Wrap calls to get_notice() and get_sxs() """
    notice = get_notice(part, notice_id)
    notice = convert_to_python(notice)
    paragraph_sxs = get_sxs(label_id, notice, fr_page)
    return notice, paragraph_sxs


def get_diff_json(regulation, older, newer):
    api = api_reader.ApiReader()
    return api.diff(regulation, older, newer)


def get_diff_applier(label_id, older, newer):
    regulation = label_id.split('-')[0]
    diff_json = get_diff_json(regulation, older, newer)
    if diff_json:
        return DiffApplier(diff_json, label_id)
