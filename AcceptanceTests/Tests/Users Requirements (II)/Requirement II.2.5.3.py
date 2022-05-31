import unittest
from Dev.ServiceLayer.SystemService import *

class MyTestCase(unittest.TestCase):
    
    def setUp(self):
        self.m=SystemService()
        self.m.initialization_of_the_system()
        self.u=self.m.get_into_the_Trading_system_as_a_guest().response
        self.m.registration_for_the_trading_system(self.u,"username","password")
        #need to login, create shop and add items to it for test
        self.m.login_into_the_trading_system(self.u,"username","password")
        self.m.shop_open(self.u,"shopname")
        self.m.adding_item_to_the_shops_stock(self.u,"itemname1","shopname","animal objects","cats and clocks",5,10)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname2","shopname","animal objects","dogs and locks",2,50)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname3","rockshop","rocks","rock collection",1,5)
        r=self.m.shopping_carts_add_item(self.u,"itemname1","shopname",1)

        
    def testPurchaseHistory(self):
        r=self.m.in_shop_purchases_history_request(self.u)
        self.assertTrue((not r.is_exception) and r.response==[])
        r=self.m.Shopping_cart_purchase(self.u)
        self.assertTrue((not r.is_exception) and r.response)
        r=self.m.in_shop_purchases_history_request("username")
        self.assertTrue((not r.is_exception) and r.response==[["shopname","itemname1"]])
        
    def testAfterRelog(self):
        self.m.logout(self.u)
        r=self.m.in_shop_purchases_history_request(self.u)
        self.assertTrue((not r.is_exception) and r.response==[])
        self.m.login_into_the_trading_system(self.u,"username","password")
        r=self.m.Shopping_cart_purchase(self.u)
        self.assertTrue((not r.is_exception) and r.response)
        r=self.m.in_shop_purchases_history_request("username")
        self.assertTrue((not r.is_exception) and r.response==[["shopname","itemname1"]])

    def testAddedAsGuest(self):
        self.m.logout(self.u)
        r=self.m.in_shop_purchases_history_request(self.u)
        self.assertTrue((not r.is_exception) and r.response==[])
        r=self.m.Shopping_cart_purchase(self.u)
        self.m.login_into_the_trading_system(self.u,"username","password")
        self.assertTrue((not r.is_exception) and r.response)
        r=self.m.in_shop_purchases_history_request("username")
        self.assertTrue((not r.is_exception) and r.response==[])
        
    def testMultiAdd(self):
        self.m.logout(self.u)
        r=self.m.in_shop_purchases_history_request(self.u)
        self.assertTrue((not r.is_exception) and r.response==[])
        self.m.shopping_carts_add_item(self.u,"itemname2","shopname",1)
        self.m.login_into_the_trading_system(self.u,"username","password")
        r=self.m.Shopping_cart_purchase(self.u)
        self.assertTrue((not r.is_exception) and r.response)
        r=self.m.in_shop_purchases_history_request("username")
        self.assertTrue((not r.is_exception) and r.response==[["shopname","itemname1","itemname2"]])

    def testMultiPurchase(self):
        self.m.logout(self.u)
        r=self.m.in_shop_purchases_history_request(self.u)
        self.assertTrue((not r.is_exception) and r.response==[])
        self.m.shopping_carts_add_item(self.u,"itemname2","shopname",1)
        r=self.m.Shopping_cart_purchase(self.u)
        self.assertTrue((not r.is_exception) and r.response)
        self.m.login_into_the_trading_system(self.u,"username","password")
        r=self.m.Shopping_cart_purchase(self.u)
        self.assertTrue((not r.is_exception) and r.response)
        r=self.m.in_shop_purchases_history_request("username")
        self.assertTrue((not r.is_exception) and r.response==[["shopname","itemname1"]])
        


if __name__ == '__main__':
    unittest.main()
