import unittest
import sys
#this is how you import from different folder in python:
sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\SHUK1')

from market import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.m=marketService()
        self.u=self.m.enter()
        self.m.register(self.u,"username","password")
    def tearDown(self):
        self.m.logout(self.u)#logout every time to allow all tests
        
    def testGood(self):
        self.assertTrue(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        self.m.login(self.u,"username","password")
        self.assertTrue(self.m.isLoggedin(u))
        
    def testLogout(self):
        self.assertTrue(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        self.m.login(self.u,"username","badpassword")
        self.assertTrue(self.m.isLoggedin(u))
        self.m.logout(self.u)
        self.assertFalse(self.m.isLoggedin(u))
        
    def testBadUser(self):
        self.assertTrue(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        self.m.login(self.u,"badusername","password")
        self.assertFalse(self.m.isLoggedin(u))
        
    def testBadPass(self):
        self.assertTrue(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        self.m.login(self.u,"username","badpassword")
        self.assertFalse(self.m.isLoggedin(u))
        
    def testDoubleLogin(self):
        self.assertTrue(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        self.m.login(self.u,"username","badpassword")
        self.assertTrue(self.m.isLoggedin(u))
        err=self.m.login(self.u,"username","badpassword")
        #should display error bus still be logged in
        self.assertTrue(self.m.isLoggedin(u))
        self.assertEqual(err,"user already logged in")
    
        
if __name__ == '__main__':
    unittest.main()
