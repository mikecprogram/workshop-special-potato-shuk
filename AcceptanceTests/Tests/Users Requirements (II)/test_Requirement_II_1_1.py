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
        self.m = SystemService()
        self.m.initialization_of_the_system()

    def testGood(self):
        u = self.m.get_into_the_Trading_system_as_a_guest()
        r = self.m.is_token_valid(u.res)
        self.assertTrue(r.res, r.exc)
        self.assertTrue(not r.isexc, r.exc)

    def testDouble(self):
        u = self.m.get_into_the_Trading_system_as_a_guest()
        r = self.m.is_token_valid(u.res)
        self.assertTrue(r.res, r.exc)
        self.assertTrue(not r.isexc, r.exc)
        u2 = self.m.get_into_the_Trading_system_as_a_guest()
        r = self.m.is_token_valid(u2.res)
        self.assertTrue(r.res, r.exc)
        self.assertTrue(not r.isexc, r.exc)
        r = self.m.is_token_valid(u.res)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        self.assertFalse(u == u2)


if __name__ == '__main__':
    unittest.main()
