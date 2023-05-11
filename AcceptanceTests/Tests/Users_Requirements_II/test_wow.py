import unittest
import sys

# this is how you import from different folder in python:
# sys.path.insert(0, r'C:\Users\USER\Desktop\workshop-special-potato-shuk\dev\ServiceLayer')
# STEP 1 : add r.exc: (self\.assertTrue\(.+(?<!r\.exc))\)$        $1,r.exc)
# STEP 2: split "and" self\.assertTrue\((.+)\sand\s(.+),\s?r.exc\)
# with
"""
self.assertTrue($2, r.exc)
        self.assertTrue($1, r.exc)
"""
from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def testGood(self):
        self.assertFalse(False)

    def testDouble(self):
        self.assertFalse(False)


if __name__ == '__main__':
    unittest.main()
