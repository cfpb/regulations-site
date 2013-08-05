from django.conf.urls import patterns, include, url

from regulations.views.chrome import RegulationSectionView, RegulationView
from regulations.views.partial import *

#Re-usable URL patterns. 
reg_version_pattern = r'(?P<reg_version>[-\d\w]+)'
part_section_pattern = r'(?P<reg_part_section>[\d]+[-][\w]+)'

urlpatterns = patterns('',
    #A regulation section with chrome
    #Example: http://.../regulation/201-4/2013-10704
    url(r'^regulation/%s/%s$' % (part_section_pattern, reg_version_pattern), 
        RegulationSectionView.as_view(), 
        name='regulation_section_view'),
    #The whole regulation with chrome
    #Example: http://.../regulation/201/2013-10704
    url(r'^regulation/(?P<reg_part>[\d]+)/%s$' % reg_version_pattern, 
        RegulationView.as_view(), 
        name='regulation_view'),

    #A regulation section without chrome
    #Example: http://.../partial/201-4/2013-10704
    url(r'^partial/(?P<label_id>[\d]+[-][\w]+)/%s$' % reg_version_pattern, 
        PartialSectionView.as_view(), 
        name='partial_section_view'),
    #An interpretation of a section/paragraph or appendix without chrome.
    #Example: http://.../partial/201-2-Interp/2013-10704
    url(r'^partial/(?P<label_id>[-\d\w]+[-]Interp)/%s' % reg_version_pattern,
        PartialInterpView.as_view(),
        name='partial_interp_view'),
    #A regulation paragraph without chrome. 
    #Example: http://.../partial/201-2-g/2013-10704
    url(r'^partial/(?P<label_id>[-\d\w]+)/%s$' % reg_version_pattern,
        PartialParagraphView.as_view(),
        name='partial_paragraph_view'),
)
