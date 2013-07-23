from django.conf.urls import patterns, include, url

from regulations.views.chrome import RegulationSectionView, RegulationView
from regulations.views.partial import PartialSectionView, PartialParagraphView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^regulation/(?P<reg_part_section>[\d]+[-][\w]+)/(?P<reg_version>[-\d\w]+)$', 
        RegulationSectionView.as_view(), 
        name='regulation_section_view'),
    url(r'^regulation/(?P<reg_part>[\d]+)/(?P<reg_version>[-\d\w]+)$', 
        RegulationView.as_view(), 
        name='regulation_view'),
    #url(r'^regulation/(?P<paragraph_id>[-\d\w]+)/(?P<reg_version>[-\d\w]+)$',
    #    RegulationParagraphView.as_view(),
    #    name='regulation_paragraph_view'),
    url(r'^partial/(?P<reg_part_section>[\d]+[-][\w]+)/(?P<reg_version>[-\d\w]+)$', 
        PartialSectionView.as_view(), 
        name='partial_section_view'),
    url(r'^partial/(?P<paragraph_id>[-\d\w]+)/(?P<reg_version>[-\d\w]+)$',
        PartialParagraphView.as_view(),
        name='partial_regulation_view'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
