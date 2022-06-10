import unittest
import sys

from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.m = SystemService()
        self.m.initialization_of_the_system()
        self.u = self.m.get_into_the_Trading_system_as_a_guest().response
        self.m.registration_for_the_trading_system(self.u, "username", "password")
        # need to login, create shop and add items to it for test

        self.m.login_into_the_trading_system(self.u, "username", "password")
        self.m.shop_open(self.u, "shopname")
        self.m.adding_item_to_the_shops_stock(self.u, "itemname1", "shopname", "animal objects", "cats and clocks", 5,
                                              10)
        self.m.adding_item_to_the_shops_stock(self.u, "itemname2", "shopname", "animal objects", "dogs and locks", 2,
                                              50)
        self.m.adding_item_to_the_shops_stock(self.u, "itemname3", "rockshop", "rocks", "rock collection", 1, 5)


    def testHasPriceAndHasAmountDiscount(self):
        self.m.add_policy(self.u, 0, "hasAmount", "itemname1", 3)  # 0 discount because the discount is not on item 1
        self.m.add_policy(self.u, 0, "hasPrice", "", 25)  # empty item so it checks total price of basket
        self.m.add_policy(self.u, 10, "isItem", "itemname2")
        self.m.compose_policy(self.u, "and", 1, 2)
        self.m.compose_policy(self.u, "and", 3, 4)
        r = self.m.get_my_policies(self.u)
        # print(r.exception, r.response)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasAmount", "itemname1", 3, 0],
                                                                [2, "hasPrice", "", 25, 0],
                                                                [3, "isItem", "itemname2", 10],
                                                                [4, "and", 1, 2],
                                                                [5, "and", 3, 4]
                                                                ])
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 5)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        # print(r.exception, r.response)
        self.assertTrue((not r.is_exception) and r.response == [["discount", 5, 10]])
        self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        r = self.m.calculate_cart_price(self.u)
        # print(r.exception,r.response)
        self.assertTrue((not r.is_exception) and r.response == 20)
        self.m.shopping_carts_add_item(self.u, "itemname2", "shopname", 5)
        r = self.m.calculate_cart_price(self.u)
        #print(r.exception, r.response)


        self.assertTrue((not r.is_exception) and r.response == 29)

    def testHasPriceAndHasAmountPurchase(self):
        self.m.add_policy(self.u, 0, "hasAmount", "itemname1", 3)
        self.m.add_policy(self.u, 0, "hasPrice", "", 25)  # empty item so it checks total price of basket
        self.m.compose_policy(self.u, "and", 1, 2)
        r = self.m.get_my_policies(self.u)
        # print(r.exception, r.response)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasAmount", "itemname1", 3, 0],
                                                                [2, "hasPrice", "", 25, 0],
                                                                [3, "and", 1, 2],
                                                                ])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 3)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        # print(r.exception, r.response)
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 3]])
        self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        r = self.m.validate_purchase_policy(self.u)
        # print(r.exception,r.response)
        self.assertTrue((not r.is_exception) and not r.response)
        self.m.shopping_carts_add_item(self.u, "itemname2", "shopname", 4)
        r = self.m.validate_purchase_policy(self.u)
        #print(r.exception, r.response)
        self.assertTrue((not r.is_exception) and r.response)


    def testHasPriceDiscount(self):
        self.m.add_policy(self.u, 20, "hasPrice", "", 25)  # empty item so it checks total price of basket

        r = self.m.get_my_policies(self.u)
        #print(r.exception, r.response)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasPrice", "", 25, 20]])
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
            # print(r.exception, r.response)
        self.assertTrue((not r.is_exception) and r.response == [["discount", 1, 20]])
        self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        r = self.m.calculate_cart_price(self.u)
        #print(r.exception,r.response)
        self.assertTrue((not r.is_exception) and r.response == 20)
        self.m.shopping_carts_add_item(self.u, "itemname2", "shopname", 5)
        r = self.m.calculate_cart_price(self.u)
        #print(r.exception, r.response)
        self.assertTrue((not r.is_exception) and r.response == 24)

    def testHasAmount(self):
        r = self.m.add_policy(self.u, 10, "hasAmount", "itemname1", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasAmount", "itemname1", 4, 10]])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 1]])
        r = self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
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
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasAmount", "itemname1", 4, 10],
                                                                [2, "hasAmount", "itemname2", 2, 10]])
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
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasAmount", "itemname1", 4, 10],
                                                                [2, "hasAmount", "itemname2", 2, 10]])
        r = self.m.compose_policy(self.u, "or", 1, 2)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasAmount", "itemname1", 4, 10],
                                                                [2, "hasAmount", "itemname2", 2, 10], [3, "or", 1, 2]])
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
        r = self.m.shopping_carts_delete_item(self.u, "itemname1", "shopname", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response == [["shopname", [["itemname2", 4]]]])
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue((not r.is_exception) and r.response)

    def testNot(self):
        # shopping bag (for "shopname") does not contain 4 items ith name "itemname1"
        r = self.m.add_policy(self.u, 10, "hasAmount", "itemname1", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasAmount", "itemname1", 4, 10]])
        r = self.m.compose_policy(self.u, "not", 1)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasAmount", "itemname1", 4, 10], [2, "not", 1]])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 2)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 2]])
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response == [["shopname", [["itemname1", 4]]]])
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue((not r.is_exception) and not r.response)
        r = self.m.shopping_carts_delete_item(self.u, "itemname1", "shopname", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response == [])
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue((not r.is_exception) and r.response)


    def testHasAmountDiscount(self):
        r = self.m.add_policy(self.u, 10, "hasAmount", "itemname1", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasAmount", "itemname1", 4, 10]])
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["discount", 1, 10]])
        r = self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.is_exception) and r.response == [["shopname", [["itemname1", 4]]]])
        r = self.m.calculate_cart_price(self.u)
        self.assertTrue((not r.is_exception) and r.response == 18) #oridinal price is 4*5=20 with 10% discount is 18

    def testComplicated(self):
        self.m.add_policy(self.u,5,"isItem", "itemname1")
        self.m.add_policy(self.u,20,"isShop")
        self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.m.add_discount_policy_to_shop(self.u, "shopname", 2)
        self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        r = self.m.calculate_cart_price(self.u)
        self.assertTrue((not r.is_exception) and r.response == 16)
        self.m.compose_policy(self.u,"add",1,2)
        self.m.add_discount_policy_to_shop(self.u, "shopname", 3)
        r = self.m.calculate_cart_price(self.u)
        self.assertTrue((not r.is_exception) and r.response == 15)
        self.m.shopping_carts_add_item(self.u, "itemname2", "shopname", 5)
        r = self.m.calculate_cart_price(self.u)
        self.assertTrue((not r.is_exception) and r.response == 23)
        self.m.add_policy(self.u, 50, "isItem", "itemname2")
        self.m.add_policy(self.u, 0, "hasAmount", "itemname1", 4)
        self.m.compose_policy(self.u, "and", 4, 5)
        self.m.add_discount_policy_to_shop(self.u, "shopname", 6)
        r = self.m.calculate_cart_price(self.u)
        self.assertTrue((not r.is_exception) and r.response == 20)
        self.m.shopping_carts_delete_item(self.u,"itemname1","shopname",1)
        r = self.m.calculate_cart_price(self.u)
        self.assertTrue((not r.is_exception) and r.response == 19.25)






if __name__ == '__main__':
    unittest.main()
