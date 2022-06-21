from dataclasses import asdict
import unittest
import sys
#this is how you import from different folder in python:
sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\dev\ServiceLayer')
from SystemService import *



class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.m=SystemService()
        self.u=self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u,"username","password")

        

        
    def testLogout(self):
        r = self.m.is_active(self.u)
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        r = self.m.is_member("username")
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        self.m.login_into_the_trading_system(self.u,"username","password")
        r = self.m.is_login(self.u)
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        self.m.logout(self.u)
        r = self.m.is_login(self.u)
        self.assertTrue((not r.isexc) and (not r.res))

    
        
if __name__ == '__main__':
    unittest.main()
