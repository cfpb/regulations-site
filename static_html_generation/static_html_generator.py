#!/usr/bin/env python

import codecs
import json
from os import mkdir, path
import shutil
import sys

import api_reader
from layers.analyses import SectionBySectionLayer
from layers.definitions import DefinitionsLayer
from layers.external_citation import ExternalCitationLayer
from layers.internal_citation import InternalCitationLayer
from layers.interpretations import InterpretationsLayer
from layers.key_terms import KeyTermsLayer
from layers.layers_applier import InlineLayersApplier
from layers.layers_applier import ParagraphLayersApplier
from layers.layers_applier import SearchReplaceLayersApplier
from layers.paragraph_markers import ParagraphMarkersLayer
from layers.toc_applier import TableOfContentsLayer
import notices
from html_builder import HTMLBuilder

import settings as app_settings
from django.conf import settings


def write_file(filename, markup):
    """ Write out a file using the UTF-8 codec. """
    f = codecs.open(filename, 'w', encoding='utf-8')
    f.write(markup)
    f.close()

if __name__ == "__main__":
    if not settings.configured:
        settings.configure(TEMPLATE_DEBUG=False, 
            TEMPLATE_LOADERS=('django.template.loaders.filesystem.Loader',), 
            TEMPLATE_DIRS = ('templates/',))

    if len(sys.argv) == 1:
        print "Usage: python static_html_generator.py regversion-to-build-from"
        print " e.g.: python static_html_generator.py 2011-31725"
        exit()

    api = api_reader.Client(app_settings.API_BASE)
    regulation, version = "1005", sys.argv[1]
    reg_json = api.regulation(regulation, version)

    inline_applier = InlineLayersApplier()
    p_applier = ParagraphLayersApplier(reg_json)
    s_applier = SearchReplaceLayersApplier()

    el = api.layer("external-citations", regulation, version)
    reference_EFT_act = ['15', '1693'] #Title 15, Section 1693 of the United States Code

    inline_applier.add_layer(ExternalCitationLayer(el, ['15', '1693']))
    il = api.layer("internal-citations", regulation, version)
    inline_applier.add_layer(InternalCitationLayer(il))

    dl = api.layer("terms", regulation, version)
    inline_applier.add_layer(DefinitionsLayer(dl))

    intl = api.layer("interpretations", regulation, version)
    p_applier.add_layer(InterpretationsLayer(intl))
    
    sxs = api.layer("analyses", regulation, version)
    p_applier.add_layer(SectionBySectionLayer(sxs))
    
    tl = api.layer("toc", regulation, version)
    p_applier.add_layer(TableOfContentsLayer(tl))

    kl = api.layer("keyterms", regulation, version)
    s_applier.add_layer(KeyTermsLayer(kl))

    pm = api.layer("paragraph-markers", regulation, version)
    s_applier.add_layer(ParagraphMarkersLayer(pm))
    
    makers_markup = HTMLBuilder(inline_applier, p_applier, s_applier)
    makers_markup.tree = reg_json
    makers_markup.generate_html()
    markup = makers_markup.render_markup()

    write_file(app_settings.OUTPUT_DIR + 'rege.html', markup)
    front_end_dir = app_settings.OUTPUT_DIR + 'front_end'
    if not path.islink(front_end_dir):
        if path.exists(front_end_dir):
            shutil.rmtree(front_end_dir)
        shutil.copytree('../front_end', front_end_dir)

    if not path.exists(app_settings.OUTPUT_DIR + 'notice'):
        mkdir(app_settings.OUTPUT_DIR + 'notice')
    for notice in notices.fetch_all(api):
        write_file(app_settings.OUTPUT_DIR + 'notice/' + 
                notice['document_number'] + ".html", notices.markup(notice))
