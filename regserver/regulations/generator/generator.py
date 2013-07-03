
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


    intl = api.layer("interpretations", regulation, version)
    intl = InterpretationsLayer(intl, version)
    p_applier.add_layer(intl)

    
    sxs = api.layer("analyses", regulation, version)
    p_applier.add_layer(SectionBySectionLayer(sxs))

    
    tl = api.layer("toc", regulation, version)
    p_applier.add_layer(TableOfContentsLayer(tl))


    kl = api.layer("keyterms", regulation, version)
    s_applier.add_layer(KeyTermsLayer(kl))


    pm = api.layer("paragraph-markers", regulation, version)
    s_applier.add_layer(ParagraphMarkersLayer(pm))


    #meta = api.layer("meta", regulation, version)
    #p_applier.add_layer(MetaLayer(meta))


    #g = api.layer("graphics", regulation, version)
    #s_applier.add_layer(GraphicsLayer(g))


    return (inline_applier, p_applier, s_applier)
