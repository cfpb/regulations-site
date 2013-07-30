import re

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

class LayerCreator(object):
    INTERNAL = 'internal-citations'
    TOC = 'toc'
    EXTERNAL = 'external-citations'
    TERMS = 'terms'
    SXS = 'analyses'
    PARAGRAPH = 'paragraph-markers'
    META = 'meta'
    GRAPHICS = 'graphics'
    INTERP = 'interpretations'
    KEY_TERMS = 'keyterms'

    LAYERS = {
        'internal': (INTERNAL,'inline'),
        'toc': (TOC,'paragraph'),
        'external': (EXTERNAL,'inline'),
        'terms': (TERMS,'inline'),
        'sxs': (SXS,'paragraph'),
        'paragraph': (PARAGRAPH,'search_replace'),
        'meta': (META, 'paragraph'),
        'graphics': (GRAPHICS,'search_replace'),
        'interp': (INTERP,'paragraph'),
        'keyterms': (KEY_TERMS, 'search_replace'),
    }

    def __init__(self):
        self.appliers = {'inline': InlineLayersApplier(), 
                        'paragraph': ParagraphLayersApplier(), 
                        'search_replace': SearchReplaceLayersApplier()}

def create_sectional_citation_layer(layer_json, version):
    """ Create an InternalCitationLayer that is aware that we're 
    loading a section at a time. """
    icl = InternalCitationLayer(layer_json)
    icl.generate_sectional = True
    icl.reg_version = version
    return icl

def add_section_internal_citations(regulation, reg_version, inline_applier):
    """ Internal citations work differently if one is loading a section 
    at a time. """
    api = api_reader.Client(settings.API_BASE)
    il = api.layer("internal-citations", regulation, reg_version)
    icl = create_sectional_citation_layer(il, reg_version)
    inline_applier.add_layer(icl)
    return inline_applier

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

def get_all_section_layers(regulation, version):
    """ When we're loading a regulation section at a time, we need to treat 
    the table of contents and internal citations layers slightly differently. """
    api = api_reader.Client(settings.API_BASE)

    inline_applier = InlineLayersApplier()
    p_applier = ParagraphLayersApplier()
    s_applier = SearchReplaceLayersApplier()

    el = api.layer("external-citations", regulation, version)
    inline_applier.add_layer(ExternalCitationLayer(el, ['15', '1693']))

    dl = api.layer("terms", regulation, version)
    inline_applier.add_layer(DefinitionsLayer(dl))

    sxs = api.layer("analyses", regulation, version)
    p_applier.add_layer(SectionBySectionLayer(sxs))

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

def get_all_layers(regulation, version):
    """ Return the three layer appliers with the available layers possible """
    api = api_reader.Client(settings.API_BASE)
    inline_applier, p_applier, s_applier = get_all_section_layers(regulation, version)

    tl = api.layer("toc", regulation, version)
    p_applier.add_layer(TableOfContentsLayer(tl))

    il = api.layer("internal-citations", regulation, version)
    inline_applier.add_layer(InternalCitationLayer(il))

    return (inline_applier, p_applier, s_applier)

def get_single_section(full_regulation, section_reference):
    """ Given a full regulation tree, return the section requested. """
    for section in full_regulation['children']:
        if section_reference == section['label']['text']:
            return section

def get_regulation_section(regulation, version, full_reference):
    """ Get a full regulation JSON tree, return the section requested. """
    full_regulation = get_regulation(regulation, version)
    single_section = get_single_section(full_regulation, full_reference)

    full_regulation['children'] = [single_section]
    return full_regulation

def get_regulation(regulation, version):
    """ Get the regulation JSON tree. Manipulate the label a bit for easier
    access in the templates."""
    api = api_reader.Client(settings.API_BASE)
    reg =  api.regulation(regulation, version)
    title = reg['label']['title']
    # up till the paren
    match = re.search('part \d+[^\w]*([^\(]*)', title, re.I)  
    if match:
        reg['label']['title_clean'] = match.group(1).strip()
    match = re.search('\(regulation (\w+)\)', title, re.I)
    if match:
        reg['label']['reg_letter'] = match.group(1)

    return reg

def get_tree_paragraph(paragraph_id, version):
    """Get a single level of the regulation tree."""
    api = api_reader.Client(settings.API_BASE)
    return api.regulation(paragraph_id, version)

def get_builder(regulation, version, inline_applier, p_applier, s_applier):
    """ Returns an HTML builder with the appliers, and the regulation tree. """
    builder = HTMLBuilder(inline_applier, p_applier, s_applier)
    builder.tree = get_regulation(regulation, version)
    return builder

def get_all_notices():
    api = api_reader.Client(settings.API_BASE)
    return notices.fetch_all(api)
