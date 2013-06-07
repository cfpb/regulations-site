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

    api = api_reader.Client(app_settings.API_BASE)

    if (not sys.argv 
    and not app_settings.TITLE_PART_NUMBER 
    or not app_settings.REG_VERSION 
    or not app_settings.ACT):
        print "Usage: python static_html_generator.py REG_VERSION TITLE_PART_NUMBER ACT"
        print "Ex: python static_html_generator.py 'remittances' '1005' '[\"15\", \"1643\"]'"
        print "Please set default parameter values in local_settings.py or include them here, as above."
        exit()

    if len(sys.argv) <= 2:
        regulation = app_settings.TITLE_PART_NUMBER
    else:
        regulation = sys.argv[2]

    if len(sys.argv) <= 1:
        version = app_settings.REG_VERSION
    else:
        version = sys.argv[1]

    reg_json = api.regulation(regulation, version)

    inline_applier = InlineLayersApplier()
    p_applier = ParagraphLayersApplier()
    s_applier = SearchReplaceLayersApplier()

    el = api.layer("external-citations", regulation, version)

    if len(sys.argv) <= 3:
        reference_EFT_act = app_settings.ACT
    else:
        reference_EFT_act = sys.argv[3]

    print "python static_html_generator.py", version, regulation, reference_EFT_act

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
    
    makers_markup = HTMLBuilder(inline_applier, p_applier, s_applier)
    intl.copy_builder(makers_markup)
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
