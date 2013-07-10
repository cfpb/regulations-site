import unittest

def suite():
    return unittest.TestLoader().discover('regulations.tests', pattern='*.py')
