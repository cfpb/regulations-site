from unittest import TestCase
from django.core.urlresolvers import reverse, resolve


class UrlTests(TestCase):
    def test_about(self):
        r = reverse('regulations.views.about.about')
        self.assertEqual(r, '/about')

    def test_chrome_section_url(self):
        r = reverse('chrome_section_view', args=('201-2', '2012-1123'))
        self.assertEqual(r, '/201-2/2012-1123')

        r = reverse(
            'chrome_section_view', args=('201-2', '2012-1123_20121011'))
        self.assertEqual(r, '/201-2/2012-1123_20121011')

    def test_sxs_url(self):
        r = reverse('chrome_sxs_view', args=('201-2-g', '2011-1738'))
        self.assertEqual(r, '/sxs/201-2-g/2011-1738')

        r = reverse('chrome_sxs_view', args=('201-2-g', '2011-1738_20110232'))
        self.assertEqual(r, '/sxs/201-2-g/2011-1738_20110232')

    def test_diff_url(self):
        r = reverse(
            'chrome_section_diff_view',
            args=('201-2', '2011-1738', '2012-22345'))
        self.assertEqual(r, '/diff/201-2/2011-1738/2012-22345')

        r = reverse(
            'chrome_section_diff_view',
            args=('201-2', '2011-1738_20121011', '2012-22345_20131022'))
        self.assertEqual(
            r, '/diff/201-2/2011-1738_20121011/2012-22345_20131022')

    def test_diff_url_supports_multiple_dashes(self):
        r = reverse(
            'chrome_section_diff_view',
            args=('201-Interp-XYZ', '2011-1738', '2012-22345'))
        self.assertEqual(r, '/diff/201-Interp-XYZ/2011-1738/2012-22345')
