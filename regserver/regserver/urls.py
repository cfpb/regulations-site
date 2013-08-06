from django.conf.urls import patterns, include, url

from regulations.views.chrome import *
from regulations.views.partial import *

#Re-usable URL patterns. 
version_pattern = r'(?P<version>[-\d\w]+)'

reg_pattern = r'(?P<label_id>[\d]+)'
section_pattern = r'(?P<label_id>[\d]+[-][\w]+)'
interp_pattern = r'(?P<label_id>[-\d\w]+[-]Interp)'
paragraph_pattern = r'(?P<label_id>[-\d\w]+)'


urlpatterns = patterns('',
    #A regulation section with chrome
    #Example: http://.../regulation/201-4/2013-10704
    url(r'^regulation/%s/%s$' % (section_pattern, version_pattern),
        ChromeSectionView.as_view(), 
        name='chrome_section_view'),
    #Interpretation of a section/paragraph or appendix
    #Example: http://.../regulation/201-4-Interp/2013-10704
    url(r'^regulation/%s/%s$' % (interp_pattern, version_pattern),
        ChromeInterpView.as_view(),
        name='chrome_interp_view'),
    #The whole regulation with chrome
    #Example: http://.../regulation/201/2013-10704
    url(r'^regulation/%s/%s$' % (reg_pattern, version_pattern), 
        ChromeRegulationView.as_view(),
        name='chrome_regulation_view'),
    #A regulation paragraph with chrome
    #Example: http://.../regulation/201-2-g/2013-10704
    url(r'^regulation/%s/%s$' % (paragraph_pattern, version_pattern),
        ChromeParagraphView.as_view(),
        name='chrome_paragraph_view'),

    #A regulation section without chrome
    #Example: http://.../partial/201-4/2013-10704
    url(r'^partial/%s/%s$' % (section_pattern, version_pattern),
        PartialSectionView.as_view(), 
        name='partial_section_view'),
    #An interpretation of a section/paragraph or appendix without chrome.
    #Example: http://.../partial/201-2-Interp/2013-10704
    url(r'^partial/%s/%s$' % (interp_pattern, version_pattern),
        PartialInterpView.as_view(),
        name='partial_interp_view'),
    #The whole regulation without chrome; not too useful; added for symmetry
    #Example: http://.../partial/201/2013-10704
    url(r'^partial/%s/%s$' % (reg_pattern, version_pattern), 
        PartialRegulationView.as_view(),
        name='partial_regulation_view'),
    #A regulation paragraph without chrome. 
    #Example: http://.../partial/201-2-g/2013-10704
    url(r'^partial/%s/%s$' % (paragraph_pattern, version_pattern),
        PartialParagraphView.as_view(),
        name='partial_paragraph_view'),
)
