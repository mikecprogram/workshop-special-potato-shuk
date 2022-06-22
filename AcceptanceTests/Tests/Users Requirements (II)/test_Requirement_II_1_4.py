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
        self.m.registration_for_the_trading_system(self.u, "username", "password")

    def tearDown(self):
        self.m.logout(self.u)  # logout every time to allow all tests

    def testGood(self):
        u = self.u
        r = self.m.is_token_valid(u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.is_member("username")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.login_into_the_trading_system(self.u, "username", "password")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.is_login(u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)

    def testBadUser(self):
        u = self.u
        r = self.m.is_token_valid(u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.is_member("username")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.login_into_the_trading_system(self.u, "badusername", "password")
        self.assertTrue(r.isexc, r.exc)
        r = self.m.is_login(u)  # Will throw exception if disconnected!
        self.assertTrue(r.isexc, r.exc)

    def testBadPass(self):
        u = self.u
        r = self.m.is_token_valid(u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.is_member("username")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.login_into_the_trading_system(self.u, "username", "badpassword")
        self.assertTrue(r.isexc, r.exc)
        r = self.m.is_login(u)  # Will throw exception if disconnected!
        self.assertTrue(r.isexc, r.exc)

    def testDoubleLogin(self):
        u = self.u
        r = self.m.is_token_valid(u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.is_member("username")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.login_into_the_trading_system(self.u, "username", "password")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.is_login(u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.login_into_the_trading_system(self.u, "username", "password")
        self.assertTrue(r.isexc, r.exc)
        r = self.m.is_login(u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)


if __name__ == '__main__':
    unittest.main()
