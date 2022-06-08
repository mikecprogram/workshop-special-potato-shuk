import unittest
import sys

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
        
        
    def testHasAmount(self):
        r = self.m.add_policy(self.u, 10, "hasAmount", "itemname1", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasAmount", "itemname1", 4, 10]])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 1]])
        r=self.m.shopping_carts_add_item(self.u,"itemname1","shopname",4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response == [["shopname", [["itemname1", 4]]]])
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue((not r.is_exception) and r.response)

    def testHasAmount2(self):
        r = self.m.add_policy(self.u, 10, "hasAmount", "itemname1", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasAmount", "itemname1", 4, 10]])
        r = self.m.add_policy(self.u, 10, "hasAmount", "itemname2", 2)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasAmount", "itemname1", 4, 10], [2, "hasAmount", "itemname2", 2, 10]])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 1]])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 2)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 1], ["purchase", 2]])
        r = self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response == [["shopname", [["itemname1", 4]]]])
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue((not r.is_exception) and not r.response)
        r = self.m.shopping_carts_add_item(self.u, "itemname2", "shopname", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response == [["shopname", [["itemname1", 4], ["itemname2", 4]]]])
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue((not r.is_exception) and r.response)

    def testOr(self):
        r = self.m.add_policy(self.u, 10, "hasAmount", "itemname1", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasAmount", "itemname1", 4, 10]])
        r = self.m.add_policy(self.u, 10, "hasAmount", "itemname2", 2)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasAmount", "itemname1", 4, 10], [2, "hasAmount", "itemname2", 2, 10]])
        r = self.m.compose_policy(self.u,"or", 1,2)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasAmount", "itemname1", 4, 10], [2, "hasAmount", "itemname2", 2, 10], [3, "or", 1, 2]])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 3)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 3]])
        r = self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response == [["shopname", [["itemname1", 4]]]])
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.shopping_carts_add_item(self.u, "itemname2", "shopname", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response == [["shopname", [["itemname1", 4], ["itemname2", 4]]]])
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.shopping_carts_delete_item(self.u,"itemname1", "shopname", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response == [["shopname", [["itemname2", 4]]]])
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue((not r.is_exception) and r.response)




if __name__ == '__main__':
    unittest.main()
