import unittest
import sys
#this is how you import from different folder in python:
sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\dev\ServiceLayer')
from SystemService import *



    def setUp(self):
        self.m=SystemService()
        self.u=self.m.get_into_the_Trading_system_as_a_guest()
        self.m.registration_for_the_trading_system(self.u,"username","password")
    def tearDown(self):
        self.m.logout(self.u)#logout every time to allow all tests
        
    def testGood(self):
        r = self.m.is_active(u)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.is_member("username")
        self.assertTrue((not r.is_exception) and r.response)
        r=self.m.login_into_the_trading_system(self.u,"username","password")
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.is_login(u)
        self.assertTrue((not r.is_exception) and r.response)
        
    def testBadUser(self):
        r = self.m.is_active(u)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.is_member("username")
        self.assertTrue((not r.is_exception) and r.response)
        r=self.m.login_into_the_trading_system(self.u,"badusername","password")
        self.assertTrue((not r.is_exception) and (not r.response))
        r = self.m.is_login(u)
        self.assertTrue((not r.is_exception) and (not r.response))
        
    def testBadPass(self):
        r = self.m.is_active(u)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.is_member("username")
        self.assertTrue((not r.is_exception) and r.response)
        r=self.m.login_into_the_trading_system(self.u,"username","badpassword")
        self.assertTrue((not r.is_exception) and (not r.response))
        r = self.m.is_login(u)
        self.assertTrue((not r.is_exception) and (not r.response))
        
    def testDoubleLogin(self):
        r = self.m.is_active(u)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.is_member("username")
        self.assertTrue((not r.is_exception) and r.response)
        r=self.m.login_into_the_trading_system(self.u,"username","password")
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.is_login(u)
        self.assertTrue((not r.is_exception) and r.response)
        r=self.m.login_into_the_trading_system(self.u,"username","password")
        self.assertTrue((not r.is_exception) and (not r.response))
        r = self.m.is_login(u)
        self.assertTrue((not r.is_exception) and (not r.response))
    
        
if __name__ == '__main__':
    unittest.main()
