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


    def testGood(self):
        self.assertFalse(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        self.m.login(self.u,"username","password")
        self.assertTrue(self.m.isLoggedin(u))
        self.u.openShop("The new Shop of Hope")
        self.assertTrue(self.u.isShopExist("The new Shop of Hope"))

    def testBad(self):
        self.assertFalse(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        self.m.login(self.u,"username","password")
        self.assertTrue(self.m.isLoggedin(u))
        self.u.openShop("The new Shop of Hope")
        self.assertFalse(self.u.isShopExist("The new Shops of Hopes"))
    
    def testBadDoubleShopName(self):
        self.assertFalse(self.m.isActive(u))
        self.assertTrue(self.m.isMember(u))
        self.m.login(self.u,"username","password")
        self.assertTrue(self.m.isLoggedin(u))
        self.u.openShop("The new Shop of Hope")
        self.assertFalse(self.u.openShop("The new Shop of Hope"))




if __name__ == '__main__':
    unittest.main()
