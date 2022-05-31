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
        self.m.shop_open(self.u,"rockshop")
        self.m.adding_item_to_the_shops_stock(self.u,"itemname1","shopname","animal objects","cats and clocks",5,10)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname2","shopname","animal objects","dogs and locks",2,50)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname3","rockshop","rocks","rock collection",1,5)
        self.m.logout(self.u)
        
        
    def testDisplayCart(self):
        self.m.shopping_carts_add_item(self.u,"itemname1","shopname",1)
        r=self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response==[["shopname",[["itemname1",1]]]])
        self.m.shopping_carts_add_item(self.u,"itemname2","shopname",1)
        self.m.shopping_carts_add_item(self.u,"itemname3","rockshop",1)
        r=self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response==[["shopname",[["itemname1",1],["itemname2",1]]],["rockshop",[["itemname3",1]]]])
        
    def testEditCart(self):
        self.m.shopping_carts_add_item(self.u,"itemname1","shopname",1)
        r=self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response==[["shopname",[["itemname1",1]]]])
        r=self.m.shopping_carts_delete_item(self.u,"itemname1","shopname",1)
        self.assertTrue((not r.is_exception) and r.response)
        r=self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response==[])
        
    def testDeleteBadAmount(self):
        self.m.shopping_carts_add_item(self.u,"itemname1","shopname",1)
        r=self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response==[["shopname",[["itemname1",1]]]])
        r=self.m.shopping_carts_delete_item(self.u,"itemname1","shopname",51)
        self.assertTrue(r.is_exception)
        r=self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response==[["shopname",[["itemname1",1]]]])
        #if deletion failed no change should be made
        
    def testDeleteBadShop(self):
        self.m.shopping_carts_add_item(self.u,"itemname1","shopname",1)
        r=self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response==[["shopname",[["itemname1",1]]]])
        r=self.m.shopping_carts_delete_item(self.u,"itemname1","badshopname",1)
        self.assertTrue(r.is_exception)
        r=self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response==[["shopname",[["itemname1",1]]]]) #if deletion failed no change should be made

    def testDeleteBadItem(self):
        self.m.shopping_carts_add_item(self.u,"itemname1","shopname",1)
        r=self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response==[["shopname",[["itemname1",1]]]])
        r=self.m.shopping_carts_delete_item(self.u,"baditemname1","shopname",1)
        self.assertTrue(r.is_exception)
        r=self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response==[["shopname",[["itemname1",1]]]]) #if deletion failed no change should be made

        
    
    
        
if __name__ == '__main__':
    unittest.main()
