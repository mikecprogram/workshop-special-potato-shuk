import unittest
import sys
#this is how you import from different folder in python:
sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\SHUK1')

from market import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.m=marketService()#new market every time
        self.u=self.m.enter()
        
    def testGood(self):
        self.assertTrue(self.m.isActive(u))
        self.m.register(self.u,"username","password")
        self.assertTrue(self.m.isMember(u))
        
    def testDoubleUser(self):
        self.assertTrue(self.m.isActive(u))
        self.m.register(self.u,"username","password")
        self.assertTrue(self.m.isMember(u))
        self.m.register(self.u,"username","password")
        self.assertTrue(self.m.isMember(u)) #still member but should error msg
        
    def testNoUser(self):
        self.assertTrue(self.m.isActive(u))
        self.m.register(self.u,"","password")
        self.assertFalse(self.m.isMember(u))
        
    def testNoPass(self):
        self.assertTrue(self.m.isActive(u))
        self.m.register(self.u,"username","")
        self.assertFalse(self.m.isMember(u))
        
if __name__ == '__main__':
    unittest.main()
