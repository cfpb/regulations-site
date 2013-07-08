
from django.conf import settings 

import api_reader
from layers.analyses import SectionBySectionLayer
from layers.definitions import DefinitionsLayer
from layers.external_citation import ExternalCitationLayer
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
from html_builder import HTMLBuilder
import notices

def add_full_toc(regulation, version, p_applier):
    """ When we are retrieving a regulation by section, we actually want the 
    full Table of Contents. """
    tl = get_table_of_contents(regulation, version)
    p_applier.add_layer(TableOfContentsLayer(tl))
    return p_applier

def get_table_of_contents(regulation, version):
    api = api_reader.Client(settings.API_BASE)
    tl = api.layer("toc", regulation, version)
    return tl

def get_all_layers(regulation, version):
    """ Return the three layer appliers with the available layers possible """
    api = api_reader.Client(settings.API_BASE)

    inline_applier = InlineLayersApplier()
    p_applier = ParagraphLayersApplier()
    s_applier = SearchReplaceLayersApplier()

    el = api.layer("external-citations", regulation, version)
    inline_applier.add_layer(ExternalCitationLayer(el, ['15', '1693']))

    il = api.layer("internal-citations", regulation, version)
    inline_applier.add_layer(InternalCitationLayer(il))

    dl = api.layer("terms", regulation, version)
    inline_applier.add_layer(DefinitionsLayer(dl))

    sxs = api.layer("analyses", regulation, version)
    p_applier.add_layer(SectionBySectionLayer(sxs))

    tl = api.layer("toc", regulation, version)
    p_applier.add_layer(TableOfContentsLayer(tl))

    kl = api.layer("keyterms", regulation, version)
    s_applier.add_layer(KeyTermsLayer(kl))

    pm = api.layer("paragraph-markers", regulation, version)
    s_applier.add_layer(ParagraphMarkersLayer(pm))

    meta = api.layer("meta", regulation, version)
    p_applier.add_layer(MetaLayer(meta))

    g = api.layer("graphics", regulation, version)
    s_applier.add_layer(GraphicsLayer(g))

    intl = api.layer("interpretations", regulation, version)
    intl = InterpretationsLayer(intl, version)
    intl.copy_builder(inline_applier, s_applier)
    p_applier.add_layer(intl)

    return (inline_applier, p_applier, s_applier)

def get_single_section(full_regulation, section_reference):
    for section in full_regulation['children']:
        if section_reference == section['label']['text']:
            return section

def get_regulation_section(regulation, version, full_reference):
    full_regulation = get_regulation(regulation, version)
    single_section = get_single_section(full_regulation, full_reference)

    full_regulation['children'] = [single_section]
    return full_regulation

def get_regulation(regulation, version):
    """ Get the regulation JSON tree. """
    api = api_reader.Client(settings.API_BASE)
    return api.regulation(regulation, version)

def get_builder(regulation, version, inline_applier, p_applier, s_applier):
    builder = HTMLBuilder(inline_applier, p_applier, s_applier)
    builder.tree = get_regulation(regulation, version)
    return builder

def get_all_notices():
    api = api_reader.Client(settings.API_BASE)
    return notices.fetch_all(api)
