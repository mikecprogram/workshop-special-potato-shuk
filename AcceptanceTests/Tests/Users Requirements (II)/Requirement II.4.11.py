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
        self.m.registration_for_the_trading_system(self.u,"username","password")
        #need to login, create shop and add items to it for test
        self.m.login_into_the_trading_system(self.u,"username","password")
        self.m.shop_open(self.u,"shopname")
    def tearDown(self):
        self.m.logout(self.u)
        
    def testGood(self):
        r = self.m.shops_roles_info_request(self.u,"shopname")
        self.assertTrue((not r.is_exception) and r.response)



if __name__ == '__main__':
    unittest.main()
