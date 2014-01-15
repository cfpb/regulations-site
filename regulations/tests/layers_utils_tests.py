from datetime import datetime
from unittest import TestCase

from regulations.generator.layers import utils


class LayerUtilsTest(TestCase):
    def test_convert_to_python(self):
        self.assertEqual("example", utils.convert_to_python("example"))
        self.assertEqual(1, utils.convert_to_python(1))
        self.assertEqual((1, 2.0, 8l), utils.convert_to_python((1, 2.0, 8l)))
        self.assertEqual(datetime(2001, 10, 11),
                         utils.convert_to_python('2001-10-11'))
        self.assertEqual(["test", "20020304", datetime(2008, 7, 20)],
                         utils.convert_to_python(['test', '20020304',
                                                  '2008-07-20']))
        self.assertEqual({'some': 3, 'then': datetime(1999, 10, 21)},
                         utils.convert_to_python({'some': 3,
                                                  'then': '1999-10-21'}))
