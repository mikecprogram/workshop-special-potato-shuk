import unittest
import sys
#this is how you import from different folder in python:
#sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\dev\ServiceLayer')

from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.m=SystemService()
        self.m.initialization_of_the_system()
        self.u=self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u,"username","password")
        #need to login, create shop and add items to it for test
        self.m.login_into_the_trading_system(self.u,"username","password")
        self.m.shop_open(self.u,"shopname")
        self.m.shop_open(self.u,"rockshop")
        lst_old = self.m.general_items_searching(self.u)
        print(lst_old.exc, lst_old.res)
        self.assertTrue(len(lst_old.res) == 0)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname1","shopname","animal objects","cats and clocks",5,10)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname2","shopname","animal objects","dogs and locks",2,50)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname3","rockshop","rocks","rock collection",1,5)
        lst_new = self.m.general_items_searching(self.u)
        #print(lst_new.exception,lst_new.response)
        self.assertTrue(len(lst_new.res) == 3)
    def tearDown(self):
        self.m.logout(self.u)
        
    def testGood(self):
        lst_old = self.m.general_items_searching(self.u)
        self.assertTrue(len(lst_old.res) == 3)
        r=self.m.deleting_item_from_shop_stock(self.u,"itemname1","shopname",10)
        #print(r.exception,r.response)
        #print(self.m.info_about_item_in_shop(self.u,"itemname1","shopname").response)
        lst_new = self.m.general_items_searching(self.u)
        self.assertTrue(len(lst_new.res) == 2)
    def testOverDelete(self):
        lst_old = self.m.general_items_searching(self.u)
        self.assertTrue(len(lst_old.res) == 3)
        self.m.deleting_item_from_shop_stock(self.u,"itemname1","shopname",11)
        lst_new = self.m.general_items_searching(self.u)
        self.assertTrue(len(lst_new.res) == 3)
    def testPartial(self):
        lst_old = self.m.general_items_searching(self.u)
        self.assertTrue(len(lst_old.res) == 3)
        self.m.deleting_item_from_shop_stock(self.u,"itemname1","shopname",9)
        lst_new = self.m.general_items_searching(self.u)
        self.assertTrue(len(lst_new.res) == 3)






if __name__ == '__main__':
    unittest.main()
