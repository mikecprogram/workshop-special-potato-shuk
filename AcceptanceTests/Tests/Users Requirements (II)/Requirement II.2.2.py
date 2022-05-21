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
        self.m.adding_item_to_the_shops_stock(self.u,"itemname1","shopname","animal objects","cats and clocks",5,10)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname2","shopname","animal objects","dogs and locks",2,50)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname3","rockshop","rocks","rock collection",1,5)
        self.m.logout(self.u)
        

        
    def testSearchName(self):
        r=self.m.general_items_searching(self.u,itemname="itemname1")
        self.assertTrue((not r.is_exception) and r.response==[["shopname","itemname1"]]) 

    def testSearchCategory(self):
        r=self.m.general_items_searching(self.u,category="animal objects")
        self.assertTrue((not r.is_exception) and r.response==[["shopname","itemname1"],["shopname","itemname2"]])
        
    def testSearchKeyword(self):
        r=self.m.general_items_searching(self.u,item_keyword="cats")
        self.assertTrue((not r.is_exception) and r.response==[["shopname","itemname1"]])

    def testSearchMaxPrice(self):
        r=self.m.general_items_searching(self.u,item_maxPrice=3)
        self.assertTrue((not r.is_exception) and r.response==[["shopname","itemname2"],["rockshop","itemname3"]])
        
    def testSearchAll(self):
        r=self.m.general_items_searching(self.u,itemname="itemname2",category="animal objects",item_keyword="dogs",item_maxPrice=3)
        self.assertTrue((not r.is_exception) and r.response==[["shopname","itemname2"]])
        
    def testSearchBad(self):
        r=self.m.general_items_searching(self.u,itemname="itemname42")
        self.assertTrue((not r.is_exception) and r.response==[]) 

    def testSearchBadNone(self):
        r=self.m.general_items_searching(self.u)
        self.assertTrue((not r.is_exception) and r.response==[])

    def testSearchExclusive(self):
        r=self.m.general_items_searching(self.u,category="animal objects",item_maxPrice=1)
        self.assertTrue((not r.is_exception) and r.response==[])
        
    def testSearchPartialDesc(self):
        r=self.m.general_items_searching(self.u,item_keyword="ock")
        self.assertTrue((not r.is_exception) and r.response==[["shopname","itemname1"],["shopname","itemname2"],["rockshop","itemname3"]])
        
    def testSearchPartialName(self):
        r=self.m.general_items_searching(self.u,item_keyword="ocks")
        self.assertTrue((not r.is_exception) and r.response==[["shopname","itemname1"],["shopname","itemname2"],["rockshop","itemname3"]])
        
    def testSearchWhitespace(self):
        r=self.m.general_items_searching(self.u,item_keyword="ock ")
        self.assertTrue((not r.is_exception) and r.response==[["rockshop","itemname3"]])
    
    
        
if __name__ == '__main__':
    unittest.main()
