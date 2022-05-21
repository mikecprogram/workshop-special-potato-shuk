import unittest
import sys
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
        r=shopping_carts_add_item(self.u,"itemname1","shopname",1)
        self.m.logout(self.u)
        
    def testPurchaseHistory(self):
        r=in_shop_purchases_history_request(self.u)
        self.assertTrue((not r.is_exception) and r.response==[])
        r=Shopping_cart_purchase(self.u)
        self.assertTrue((not r.is_exception) and r.response)
        r=in_shop_purchases_history_request(self.u)
        self.assertTrue((not r.is_exception) and r.response==[["shopname","itemname1"]])
        


if __name__ == '__main__':
    unittest.main()
