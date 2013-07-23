from django.conf.urls import patterns, include, url

from regulations.views.chrome import RegulationSectionView, RegulationView
from regulations.views.partial import PartialSectionView, PartialParagraphView

#Re-usable URL patterns. 
reg_version_pattern = r'(?P<reg_version>[-\d\w]+)'
part_section_pattern = r'(?P<reg_part_section>[\d]+[-][\w]+)'

urlpatterns = patterns('',
    #A regulation section with chrome
    url(r'^regulation/%s/%s$' % (part_section_pattern, reg_version_pattern), 
        RegulationSectionView.as_view(), 
        name='regulation_section_view'),
    #The whole regulation with chrome
    url(r'^regulation/(?P<reg_part>[\d]+)/%s$' % reg_version_pattern, 
        RegulationView.as_view(), 
        name='regulation_view'),
    #A regulation section without chrome
    url(r'^partial/%s/%s$' % (part_section_pattern, reg_version_pattern), 
        PartialSectionView.as_view(), 
        name='partial_section_view'),
    #A regulation paragraph without chrome. 
    url(r'^partial/(?P<paragraph_id>[-\d\w]+)/%s$' % reg_version_pattern,
        PartialParagraphView.as_view(),
        name='partial_regulation_view'),
)
