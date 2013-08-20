from unittest import TestCase
from regulations.generator import reg


class RegTest(TestCase):
    def test_try_split(self):
        self.assertEqual(['a', 'xb'], reg.try_split('a:xb', ('|', ':', 'x')))

    def test_appendix_supplement_ap(self):
        elements = reg.appendix_supplement({
            'index': ['204', 'A'],
            'title': 'Appendix A to 204-First Appendix'})
        self.assertTrue(elements['is_appendix'])
