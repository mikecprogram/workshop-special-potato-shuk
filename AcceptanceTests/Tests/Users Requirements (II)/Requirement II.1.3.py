import unittest
import sys
#this is how you import from different folder in python:
sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\dev\ServiceLayer')
from SystemService import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.m=SystemService()
        self.u=self.m.get_into_the_Trading_system_as_a_guest()
        
    def testGood(self):
        r = self.m.is_active(u)
        self.assertTrue((not r.is_exception) and r.response)
        r=self.m.registration_for_the_trading_system(self.u,"username","password")
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.is_member(u)
        self.assertTrue((not r.is_exception) and r.response)
        
    def testDoubleUser(self):
        r = self.m.is_active(u)
        self.assertTrue((not r.is_exception) and r.response)
        r=self.m.registration_for_the_trading_system(self.u,"username","password")
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.is_member("username")
        self.assertTrue((not r.is_exception) and r.response)
        r=self.m.registration_for_the_trading_system(self.u,"username","password")
        self.assertTrue((not r.is_exception) and (not r.response))
        r = self.m.is_member("username")
        self.assertTrue((not r.is_exception) and r.response)
        
    def testNoUser(self):
        r = self.m.is_active(u)
        self.assertTrue((not r.is_exception) and r.response)
        r=self.m.registration_for_the_trading_system(self.u,"","password")
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.is_member("")
        self.assertTrue((not r.is_exception) and r.response)
        
    def testNoPass(self):
        r = self.m.is_active(u)
        self.assertTrue((not r.is_exception) and r.response)
        r=self.m.registration_for_the_trading_system(self.u,"username","")
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.is_member("username")
        self.assertTrue((not r.is_exception) and r.response)
        
if __name__ == '__main__':
    unittest.main()
