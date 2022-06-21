import unittest
from Dev.ServiceLayer.SystemService import *

class MyTestCase(unittest.TestCase):
    
    def setUp(self):
        self.m=SystemService()
        self.m.initialization_of_the_system()
        self.u=self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u,"username","password")

    def testGood(self):
        self.assertFalse(self.m.isActive(self.u))
        self.assertTrue(self.m.isMember(self.u),r.exc)
        self.m.login(self.u,"username","password")
        self.assertTrue(self.m.isActive(self.u),r.exc)
        self.assertTrue(self.m.isMember(self.u),r.exc)
        self.m.logout(self.u)
        self.assertFalse(self.m.isLoggedin(self.u))
        self.assertTrue(self.m.isMember(self.u),r.exc)

    def testBadLogout(self):
        self.assertFalse(self.m.isActive(self.u))
        self.assertTrue(self.m.isMember(self.u),r.exc)
        self.m.login(self.u,"username","password")
        self.assertTrue(self.m.isActive(self.u),r.exc)
        self.assertTrue(self.m.isMember(self.u),r.exc)
        #self.m.logout(self.u) # the logout not working
        self.assertTrue(self.m.isLoggedin(self.u),r.exc)
        self.assertTrue(self.m.isMember(self.u),r.exc)

    def testBadLogoutNoLogin(self):
        self.assertFalse(self.m.isActive(self.u))
        self.assertTrue(self.m.isMember(self.u),r.exc)
        #self.m.login(self.u,"username","password")
        self.assertFalse(self.m.isActive(self.u))
        self.assertTrue(self.m.isMember(self.u),r.exc)
        self.m.logout(self.u) # the logout not working
        self.assertFalse(self.m.isLoggedin(self.u))
        self.assertTrue(self.m.isMember(self.u),r.exc)

    def testBadLogoutDouble(self):
        self.assertFalse(self.m.isActive(self.u))
        self.assertTrue(self.m.isMember(self.u),r.exc)
        self.m.login(self.u,"username","password")
        self.assertTrue(self.m.isActive(self.u),r.exc)
        self.assertTrue(self.m.isMember(self.u),r.exc)
        self.m.logout(self.u)
        self.assertFalse(self.m.isLoggedin(self.u))
        self.assertTrue(self.m.isMember(self.u),r.exc)
        self.m.logout(self.u)
        self.assertFalse(self.m.isLoggedin(self.u))
        self.assertTrue(self.m.isMember(self.u),r.exc)


if __name__ == '__main__':
    unittest.main()
