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
    """ This lets us dynamically load layers by name. """
    INTERNAL = 'internal'
    TOC = 'toc'
    EXTERNAL = 'external'
    TERMS = 'terms'
    SXS = 'sxs'
    PARAGRAPH = 'paragraph'
    META = 'meta'
    GRAPHICS = 'graphics'
    INTERP = 'interp'
    KEY_TERMS = 'keyterms'

    LAYERS = {
        INTERNAL: ('internal-citations','inline', InternalCitationLayer),
        TOC: ('toc','paragraph', TableOfContentsLayer),
        EXTERNAL: ('external-citations','inline', ExternalCitationLayer),
        TERMS: ('terms','inline', DefinitionsLayer),
        SXS: ('analyses','paragraph', SectionBySectionLayer),
        PARAGRAPH: ('paragraph-markers','search_replace', ParagraphMarkersLayer),
        META: ('meta', 'paragraph', MetaLayer),
        GRAPHICS: ('graphics','search_replace', GraphicsLayer),
        INTERP: ('interpretations','paragraph', InterpretationsLayer),
        KEY_TERMS: ('keyterms', 'search_replace', KeyTermsLayer),
    }

    SPECIAL_CASES = [EXTERNAL, INTERP]

    def __init__(self):
        self.appliers = {'inline': InlineLayersApplier(), 
                        'paragraph': ParagraphLayersApplier(), 
                        'search_replace': SearchReplaceLayersApplier()}

        self.api = api_reader.Client(settings.API_BASE)

    def get_layer_json(self, api_name, regulation, version):
        """ Hit the API to retrieve the regulation JSON. """
        return self.api.layer(api_name, regulation, version)

    def add_layer(self,layer_name,regulation, version):
        """ Add a normal layer (no special handling required) to the applier. """
        if layer_name in LayerCreator.LAYERS:
        #if layer_name in LayerCreator.LAYERS and (not in LayerCreator.SPECIAL_CASES):
            api_name, applier_type, layer_class = LayerCreator.LAYERS[layer_name]
            layer_json = self.get_layer_json(api_name, regulation, version)
            layer = layer_class(layer_json)
            self.appliers[applier_type].add_layer(layer)

    def add_external_citation_layer(self, regulation, version):
        """ Add the external citation layer to the appropriate applier. The
        external citation layer needs to be initialized with the Act reference.
        Hence it needs to be dealt with uniquely. """

        api_name, applier_type, layer_class = LayerCreator.LAYERS[LayerCreator.EXTERNAL]

        layer_json = self.get_layer_json(api_name, regulation, version)
        layer = ExternalCitationLayer(layer_json, ['15', '1693'])
        applier_type = LayerCreator.LAYERS[LayerCreator.EXTERNAL][1]
        self.appliers[applier_type].add_layer(layer)
    
    def add_interpretation_layer(self, regulation, version):
        """ Add the interpretations layer to the appropriate applier. The
        interpretations layer needs to have the other appliers. Hence it needs
        to be dealt with uniquely. """
        api_name, applier_type, layer_class = LayerCreator.LAYERS[LayerCreator.INTERP]
        layer_json = self.get_layer_json(api_name, regulation, version)
        layer = layer_class(layer_json, version)
        layer.copy_builder(self.appliers['inline'], self.appliers['search_replace'])
        self.appliers[applier_type].add_layer(layer)
    
    @staticmethod
    def create_sectional_citation_layer(layer_json, version):
        """ Create an InternalCitationLayer that is aware that we're 
        loading a section at a time. """
        icl = InternalCitationLayer(layer_json)
        icl.generate_sectional = True
        icl.reg_version = version
        return icl

    def add_sectional_internal_layer(self, regulation, version):
        api_name, applier_type, layer_class = LayerCreator.LAYERS[LayerCreator.INTERNAL]
        layer_json = self.get_layer_json(api_name, regulation, version)
        layer = LayerCreator.create_sectional_citation_layer(layer_json, version)
        self.appliers[applier_type].add_layer(layer)

    def add_layers(self, layer_names, regulation, version, sectional=False):
        #This doesn't deal with sectional interpretations yet. 
        #we'll have to do that. 
        last = []
        for layer_name in layer_names:
            if layer_name == LayerCreator.INTERP:
                last.append(LayerCreator.INTERP)
            elif layer_name == LayerCreator.EXTERNAL:
                self.add_external_citation_layer(regulation, version)
            elif layer_name == LayerCreator.INTERNAL and sectional:
                self.add_sectional_internal_layer(regulation, version)
            else:
                self.add_layer(layer_name, regulation, version)

        if len(last) > 0:
            self.add_interpretation_layer(regulation, version)

    def get_appliers(self):
        """ Return the appliers. """
        return (self.appliers['inline'], 
                self.appliers['paragraph'], 
                self.appliers['search_replace'])

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
