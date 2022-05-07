import unittest
import sys
from SHUK1.stock import stock
from SHUK1.stockItem import stockItem
#this is how you import from different folder in python:
sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\SHUK1')

from market import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.m=marketService()
        self.u=self.m.enter()
        self.m.register(self.u,"username","password")
        self.m.login(self.u,"username","password")
        self.u.openShop("The new Shop of Hope")
    def tearDown(self):
        self.m.logout(self.u)#logout every time to allow all tests
        
    def testGood(self):
        self.assertTrue(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        self.m.login(self.u,"username","password")
        self.assertTrue(self.m.isLoggedin(u))
        self.u.getShop("The new Shop of Hope").addItemToStock( stockItem("banana","yellow great banana:","123"))
        self.assertTrue(self.u.getShop("The new Shop of Hope").StockSize()>0)
        self.u.getShop("The new Shop of Hope").removeItemFromStock("123")
        self.assertFalse(self.u.getShop("The new Shop of Hope").StockSize()>0)
        

    def testBad(self):
        self.assertTrue(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        self.m.login(self.u,"username","password")
        self.assertTrue(self.m.isLoggedin(u))
        self.u.getShop("The new Shop of Hope").addItemToStock( stockItem("banana","yellow great banana:","123"))
        self.assertFalse(self.u.getShop("The new Shop of Hope").StockSize()>0)
        self.u.getShop("The new Shop of Hope").removeItemFromStock("123")
        self.assertTrue(self.u.getShop("The new Shop of Hope").StockSize()>0)


if __name__ == '__main__':
    unittest.main()
