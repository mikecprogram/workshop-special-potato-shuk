import unittest
from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.m = SystemService()
        self.m.initialization_of_the_system()
        self.u = self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u, "username", "password")

    def testGood(self):
        self.assertTrue(self.m.is_token_valid(self.u).res)
        self.assertTrue(self.m.is_member("username").res)
        self.m.login_into_the_trading_system(self.u, "username", "password")
        self.assertTrue(self.m.is_token_valid(self.u).res)
        self.assertTrue(self.m.is_member("username").res)
        self.m.logout(self.u)
        self.assertFalse(self.m.is_login(self.u).res)
        self.assertTrue(self.m.is_member("username").res)

    def testBadLogout(self):
        self.assertTrue(self.m.is_token_valid(self.u).res)
        self.assertTrue(self.m.is_member("username").res)
        self.m.login_into_the_trading_system(self.u, "username", "password")
        self.assertTrue(self.m.is_token_valid(self.u).res)
        self.assertTrue(self.m.is_member("username").res)
        # self.m.logout(self.u) # the logout not working
        self.assertTrue(self.m.is_login(self.u).res)
        self.assertTrue(self.m.is_member("username").res)

    def testBadLogoutNoLogin(self):
        self.assertTrue(self.m.is_token_valid(self.u).res)
        self.assertTrue(self.m.is_member("username").res)
        # self.m.login(self.u,"username","password")
        self.assertTrue(self.m.is_token_valid(self.u).res)
        self.assertTrue(self.m.is_member("username").res)
        self.m.logout(self.u)  # the logout not working
        self.assertFalse(self.m.is_login(self.u).res)
        self.assertTrue(self.m.is_member("username").res)

    def testBadLogoutDouble(self):
        self.assertTrue(self.m.is_token_valid(self.u).res)
        self.assertTrue(self.m.is_member("username").res)
        self.m.login_into_the_trading_system(self.u, "username", "password")
        self.assertTrue(self.m.is_token_valid(self.u).res)
        self.assertTrue(self.m.is_member("username").res)
        self.m.logout(self.u)
        self.assertFalse(self.m.is_login(self.u).res)
        self.assertTrue(self.m.is_member("username").res)
        self.m.logout(self.u)
        self.assertFalse(self.m.is_login(self.u).res)
        self.assertTrue(self.m.is_member("username").res)


if __name__ == '__main__':
    unittest.main()
