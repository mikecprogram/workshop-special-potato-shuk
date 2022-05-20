import unittest
import sys
#this is how you import from different folder in python:
sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\SHUK1')

from SystemService import *

class MyTestCase(unittest.TestCase):
    
    def setUp(self):
        self.m=SystemService()
        self.u=self.m.get_into_the_Trading_system_as_a_guest()
        self.m.registration_for_the_trading_system(self.u,"username","password")

    def testGood(self):
        self.assertFalse(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        self.m.login(self.u,"username","password")
        self.assertTrue(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        self.m.logout(self.u)
        self.assertFalse(self.m.isLoggedin(u))
        self.assertTrue(self.m.isMember(u))

    def testBadLogout(self):
        self.assertFalse(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        self.m.login(self.u,"username","password")
        self.assertTrue(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        #self.m.logout(self.u) # the logout not working
        self.assertTrue(self.m.isLoggedin(u))
        self.assertTrue(self.m.isMember(u))

    def testBadLogoutNoLogin(self):
        self.assertFalse(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        #self.m.login(self.u,"username","password")
        self.assertFalse(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        self.m.logout(self.u) # the logout not working
        self.assertFalse(self.m.isLoggedin(u))
        self.assertTrue(self.m.isMember(u))

    def testBadLogoutDouble(self):
        self.assertFalse(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        self.m.login(self.u,"username","password")
        self.assertTrue(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        self.m.logout(self.u)
        self.assertFalse(self.m.isLoggedin(u))
        self.assertTrue(self.m.isMember(u))
        self.m.logout(self.u)
        self.assertFalse(self.m.isLoggedin(u))
        self.assertTrue(self.m.isMember(u))

    def happyCase(self):
        pass

    def sadCase(self):
        pass

    def badCase(self):
        pass


if __name__ == '__main__':
    unittest.main()
