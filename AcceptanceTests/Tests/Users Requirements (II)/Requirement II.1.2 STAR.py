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

        

        
    def testLogout(self):
        self.assertTrue(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        self.m.login(self.u,"username","badpassword")
        self.assertTrue(self.m.isLoggedin(u))
        self.m.logout(self.u)
        self.assertFalse(self.m.isLoggedin(u))
        

    
        
if __name__ == '__main__':
    unittest.main()
