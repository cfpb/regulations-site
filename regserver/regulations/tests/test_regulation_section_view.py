from django.test import SimpleTestCase
from regulations.views import RegulationSectionView

class RegulationSectionViewTestCase(SimpleTestCase):
    def test_get_regulation_part(self):
        part = RegulationSectionView.get_regulation_part('202-12-13')
        self.assertEquals(part, '202')

    def test_get_regulation_part_single(self):
        part = RegulationSectionView.get_regulation_part('202')
        self.assertEquals(part, '202')

