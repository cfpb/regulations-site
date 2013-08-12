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

    SPECIAL_CASES = [INTERP]

    def __init__(self):
        self.appliers = {'inline': InlineLayersApplier(), 
                        'paragraph': ParagraphLayersApplier(), 
                        'search_replace': SearchReplaceLayersApplier()}

        self.api = api_reader.Client(settings.API_BASE)

    def get_layer_json(self, api_name, regulation, version):
        """ Hit the API to retrieve the regulation JSON. """
        return self.api.layer(api_name, regulation, version)

    def add_layer(self,layer_name,regulation, version, sectional=False):
        """ Add a normal layer (no special handling required) to the applier. """
        if layer_name.lower() in LayerCreator.LAYERS and \
                layer_name not in LayerCreator.SPECIAL_CASES:
            api_name, applier_type, layer_class = LayerCreator.LAYERS[layer_name]
            layer_json = self.get_layer_json(api_name, regulation, version)
            layer = layer_class(layer_json)

            if sectional and hasattr(layer, 'sectional'):
                layer.sectional = sectional
            if hasattr(layer, 'version'):
                layer.version = version

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

    def add_layers(self, layer_names, regulation, version, sectional=False):
        #This doesn't deal with sectional interpretations yet. 
        #we'll have to do that. 
        last = []
        for layer_name in layer_names:
            if layer_name == LayerCreator.INTERP:
                last.append(LayerCreator.INTERP)
            else:
                self.add_layer(layer_name, regulation, version, sectional)

        if len(last) > 0:
            self.add_interpretation_layer(regulation, version)

    def get_appliers(self):
        """ Return the appliers. """
        return (self.appliers['inline'], 
                self.appliers['paragraph'], 
                self.appliers['search_replace'])


def get_regulation(regulation, version):
    """ Get the regulation JSON tree. Manipulate the label a bit for easier
    access in the templates."""
    api = api_reader.Client(settings.API_BASE)
    reg =  api.regulation(regulation, version)
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
