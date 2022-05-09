from hashlib import new
import unittest
import sys
from SHUK1.stock import stock
from SHUK1.stockItem import stockItem
#this is how you import from different folder in python:
sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\SHUK1')

from SystemService import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.m=SystemService()
        self.u=self.m.get_into_the_Trading_system_as_a_guest()
        self.u2=self.m.get_into_the_Trading_system_as_a_guest()
        self.m.registration_for_the_trading_system(self.u,"username","password")
        self.m.registration_for_the_trading_system(self.u,"username2","password2")
        #need to login, create shop and add items to it for test
        self.m.login_into_the_trading_system(self.u,"username","password")
        self.m.login_into_the_trading_system(self.u2,"username2","password2")
        self.m.shop_open(self.u,"shopname")
    def tearDown(self):
        self.m.logout(self.u)
        self.m.logout(self.u2)
        
    def testGood(self):
        r = self.m.shop_manager_assignment(self.u,"shopname","username2")
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.shop_manager_permissions_check(self.u,"username2","shopname")
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.shop_manager_permissions_add(self.u,"username2",1,"shopname")


if __name__ == '__main__':
    unittest.main()
