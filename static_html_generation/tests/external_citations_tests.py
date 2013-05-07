from unittest import TestCase
from mock import Mock, patch

from layers.external_citation import ExternalCitationLayer

class ExternalCitationsTest(TestCase):
    def test_statues_at_large_link(self):
        text = '124 Stat. 2859'
        citation = text.split()
        link = ExternalCitationLayer.generate_statutes_at_large_link(text, citation)
        real_link = 'http://api.fdsys.gov/link?collection=plaw&statutecitation=124+stat+2859'
        self.assertEqual(link, real_link)
