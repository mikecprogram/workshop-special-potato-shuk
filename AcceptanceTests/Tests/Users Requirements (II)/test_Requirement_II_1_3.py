import unittest
import sys
# this is how you import from different folder in python:
# sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\dev\ServiceLayer')
from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.m = SystemService()
        self.m.initialization_of_the_system()
        self.u = self.m.get_into_the_Trading_system_as_a_guest().res

    def testGood(self):
        r = self.m.is_active(self.u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.registration_for_the_trading_system(self.u, "username", "password")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.is_member("username")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)

    def testDoubleUser(self):
        r = self.m.is_active(self.u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.registration_for_the_trading_system(self.u, "username", "password")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.is_member("username")

        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.registration_for_the_trading_system(self.u, "username", "password")
        self.assertTrue(r.isexc, r.exc)
        r = self.m.is_member("username")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)

    def testNoUser(self):
        r = self.m.is_active(self.u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.registration_for_the_trading_system(self.u, "", "password")
        self.assertTrue(r.isexc, r.exc)
        r = self.m.is_member("")
        self.assertTrue((not r.res), r.exc)
        self.assertTrue((not r.isexc), r.exc)

    def testNoPass(self):
        r = self.m.is_active(self.u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.registration_for_the_trading_system(self.u, "username", "")
        self.assertTrue(r.isexc, r.exc)
        r = self.m.is_member("username")
        self.assertTrue((not r.res), r.exc)
        self.assertTrue((not r.isexc), r.exc)


if __name__ == '__main__':
    unittest.main()
