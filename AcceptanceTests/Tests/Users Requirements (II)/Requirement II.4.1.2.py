import unittest
import sys
#this is how you import from different folder in python:
sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\dev\ServiceLayer')

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
        
    def testEmpty(self): #find all items with empty search
        lst_old = self.m.general_items_searching(self.u)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname1","shopname","animal objects","cats and clocks",5,10)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname2","shopname","animal objects","dogs and locks",2,50)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname3","rockshop","rocks","rock collection",1,5)
        lst_new = self.m.general_items_searching(self.u)
        self.assertTrue(lst_old.response.count == 0 and lst_new.response.count == 3)

    def testByName(self): 
        lst_old = self.m.general_items_searching(self.u,item_name="itemname1")
        self.m.adding_item_to_the_shops_stock(self.u,"itemname1","shopname","animal objects","cats and clocks",5,10)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname2","shopname","animal objects","dogs and locks",2,50)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname3","rockshop","rocks","rock collection",1,5)
        lst_new = self.m.general_items_searching(self.u,item_name="itemname1")
        self.assertTrue(lst_old.response.count == 0 and lst_new.response.count == 1)
        
    def testByCategory(self): 
        lst_old = self.m.general_items_searching(self.u,category="animal objects")
        self.m.adding_item_to_the_shops_stock(self.u,"itemname1","shopname","animal objects","cats and clocks",5,10)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname2","shopname","animal objects","dogs and locks",2,50)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname3","rockshop","rocks","rock collection",1,5)
        lst_new = self.m.general_items_searching(self.u,category="animal objects")
        self.assertTrue(lst_old.response.count == 0 and lst_new.response.count == 2)

    def testByKeywoerd(self): 
        lst_old = self.m.general_items_searching(self.u,item_keyword="cats and dogs")
        self.m.adding_item_to_the_shops_stock(self.u,"itemname1","shopname","animal objects","cats and clocks",5,10)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname2","shopname","animal objects","dogs and locks",2,50)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname3","rockshop","rocks","rock collection",1,5)
        lst_new = self.m.general_items_searching(self.u,item_keyword="cats and dogs")
        self.assertTrue(lst_old.response.count == 0 and lst_new.response.count == 1)
        
    def testByKeywoerdPartial(self): 
        lst_old = self.m.general_items_searching(self.u,item_keyword="lock")
        self.m.adding_item_to_the_shops_stock(self.u,"itemname1","shopname","animal objects","cats and clocks",5,10)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname2","shopname","animal objects","dogs and locks",2,50)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname3","rockshop","rocks","rock collection",1,5)
        lst_new = self.m.general_items_searching(self.u,item_keyword="lock")
        self.assertTrue(lst_old.response.count == 0 and lst_new.response.count == 2)

    def testByKeywoerdPartial2(self): 
        lst_old = self.m.general_items_searching(self.u,item_keyword="ock")
        self.m.adding_item_to_the_shops_stock(self.u,"itemname1","shopname","animal objects","cats and clocks",5,10)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname2","shopname","animal objects","dogs and locks",2,50)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname3","rockshop","rocks","rock collection",1,5)
        lst_new = self.m.general_items_searching(self.u,item_keyword="ock")
        self.assertTrue(lst_old.response.count == 0 and lst_new.response.count == 3)
        
    def testByPrice(self): 
        lst_old = self.m.general_items_searching(self.u,item_maxPrice=10)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname1","shopname","animal objects","cats and clocks",5,10)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname2","shopname","animal objects","dogs and locks",2,50)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname3","rockshop","rocks","rock collection",1,5)
        lst_new = self.m.general_items_searching(self.u,item_maxPrice=10)
        self.assertTrue(lst_old.response.count == 0 and lst_new.response.count == 2)




if __name__ == '__main__':
    unittest.main()
