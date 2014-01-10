from datetime import datetime
from unittest import TestCase

from regulations.generator.layers.utils import *

class LayerUtilsTest(TestCase):
    
    def test_convert_to_python(self):
        self.assertEqual("example", convert_to_python("example"))
        self.assertEqual(1, convert_to_python(1))
        self.assertEqual((1, 2.0, 8l), convert_to_python((1, 2.0, 8l)))
        self.assertEqual(datetime(2001, 10, 11),
                         convert_to_python('2001-10-11'))
        self.assertEqual(["test", "20020304", datetime(2008, 7, 20)],
                         convert_to_python(['test', '20020304', '2008-07-20']))
        self.assertEqual({'some': 3, 'then': datetime(1999, 10, 21)},
                         convert_to_python({'some': 3, 'then': '1999-10-21'}))

    def test_regurlof(self):
        url = RegUrl.of(['303', '1'], 'vvv', False)
        self.assertEquals('#303-1', url)

        url = RegUrl.of(['303', '1', 'b'], 'vvv', False)
        self.assertEquals('#303-1-b', url)

        url = RegUrl.of(['303'], 'vvv', False)
        self.assertEquals('#303', url)

        url = RegUrl.of(['303', '1', 'b'], 'vvv', True)
        self.assertEquals('/303-1/vvv#303-1-b', url)

        self.assertTrue('999-88/verver#999-88-e' in
                        RegUrl.of(['999', '88', 'e'], 'verver', True))
        self.assertTrue('999-Interp/verver#999-88-e-Interp-1' in
                        RegUrl.of(['999', '88', 'e', 'Interp', '1'],
                                  'verver', True))
        self.assertTrue('999-Interp/verver#999-Interp' in
                        RegUrl.of(['999', 'Interp'], 'verver', True))
        self.assertEqual(
            '#999-88-e', RegUrl.of(['999', '88', 'e'], 'verver', False))

        self.assertEqual(
            '#999-Subpart-Interp',
            RegUrl.of(['999', 'Subpart', 'Interp'], 'verver', False))
        self.assertEqual(
            '#999-Subpart-A-Interp',
            RegUrl.of(['999', 'Subpart', 'A', 'Interp'], 'verver', False))
        self.assertEqual(
            '#999-Appendices-Interp',
            RegUrl.of(['999', 'Appendices', 'Interp'], 'verver', False))
