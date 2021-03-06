import unittest
import sys

from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.m = SystemService()
        self.m.initialization_of_the_system()
        self.u = self.m.get_into_the_Trading_system_as_a_guest().res
        self.u2 = self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u, "username", "password")
        self.m.registration_for_the_trading_system(self.u2, "ownername", "password")
        # need to login, create shop and add items to it for test

        self.m.login_into_the_trading_system(self.u, "username", "password")
        self.m.shop_open(self.u, "shopname")
        r = self.m.shop_owner_assignment(self.u,"shopname", "ownername")
        self.m.shop_open(self.u, "rockshop")
        self.m.adding_item_to_the_shops_stock(self.u, "itemname1", "shopname", "animal objects", "cats and clocks", 5,
                                              30)
        self.m.adding_item_to_the_shops_stock(self.u, "itemname2", "shopname", "animal objects", "dogs and locks", 2,
                                              50)
        self.m.adding_item_to_the_shops_stock(self.u, "itemname3", "rockshop", "rocks", "rock collection", 1, 5)

    def testHasPriceAndHasAmountDiscount(self):
        self.m.add_policy(self.u, "shopname", 0, "hasAmount", "itemname1", 3)  # 0 discount because the discount is not on item 1
        self.m.add_policy(self.u, "shopname", 0, "hasPrice", "", 25)  # empty item so it checks total price of basket
        self.m.add_policy(self.u, "shopname", 10, "isItem", "itemname2")
        self.m.compose_policy(self.u, "shopname", "and", 1, 2)
        self.m.compose_policy(self.u, "shopname", "and", 3, 4)
        r = self.m.get_my_policies(self.u, "shopname")
        self.assertTrue((not r.isexc) and r.res == [[1, "hasAmount", "itemname1", 3, 0],
                                                    [2, "hasPrice", "", 25, 0],
                                                    [3, "isItem", "itemname2", 10],
                                                    [4, "and", 1, 2],
                                                    [5, "and", 3, 4]
                                                    ])
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 5)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        # print(r.exception, r.response)
        self.assertEqual(r.res, [["discount", 5, 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        r = self.m.calculate_cart_price(self.u)
        # print(r.exception,r.response)
        self.assertEqual(r.res, 20, r.res)
        self.assertTrue((not r.isexc), r.exc)
        self.m.shopping_carts_add_item(self.u, "itemname2", "shopname", 5)
        r = self.m.calculate_cart_price(self.u)
        # print(r.exception, r.response)

        self.assertEqual(r.res, 29, r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testHasPriceAndHasAmountPurchase(self):
        self.m.add_policy(self.u, "shopname", 0, "hasAmount", "itemname1", 3)
        self.m.add_policy(self.u, "shopname", 0, "hasPrice", "", 25)  # empty item so it checks total price of basket
        self.m.compose_policy(self.u, "shopname", "and", 1, 2)
        r = self.m.get_my_policies(self.u, "shopname")
        self.assertTrue((not r.isexc) and r.res == [[1, "hasAmount", "itemname1", 3, 0],
                                                    [2, "hasPrice", "", 25, 0],
                                                    [3, "and", 1, 2],
                                                    ])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 3)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        # print(r.exception, r.response)
        self.assertEqual(r.res, [["purchase", 3]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        r = self.m.validate_purchase_policy(self.u)
        # print(r.exception,r.response)
        self.assertTrue(not r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        self.m.shopping_carts_add_item(self.u, "itemname2", "shopname", 4)
        r = self.m.validate_purchase_policy(self.u)
        # print(r.exception, r.response)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)

    def testHasPriceDiscount(self):
        self.m.add_policy(self.u, "shopname", 20, "hasPrice", "", 25)  # empty item so it checks total price of basket

        r = self.m.get_my_policies(self.u, "shopname")
        # print(r.exception, r.response)
        self.assertEqual(r.res, [[1, "hasPrice", "", 25, 20]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        # print(r.exception, r.response)
        self.assertEqual(r.res, [["discount", 1, 20]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        r = self.m.calculate_cart_price(self.u)
        # print(r.exception,r.response)
        self.assertEqual(r.res, 20, r.res)
        self.assertTrue((not r.isexc), r.exc)
        self.m.shopping_carts_add_item(self.u, "itemname2", "shopname", 5)
        r = self.m.calculate_cart_price(self.u)
        # print(r.exception, r.response)
        self.assertEqual(r.res, 24, r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testHasAmount(self):
        r = self.m.add_policy(self.u, "shopname", 10, "hasAmount", "itemname1", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u, "shopname")
        self.assertEqual(r.res, [[1, "hasAmount", "itemname1", 4, 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertEqual(r.res, [["purchase", 1]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertTrue(not r.isexc, r.exc)
        self.assertEqual(r.res , {"shopname": [{"name": "itemname1",
                                               "price": 5.0,
                                               "amount": 30,
                                               "count": 4,
                                               "category": "animal objects",
                                               "description": "cats and clocks"}]})
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)

    def testHasAmount2(self):
        r = self.m.add_policy(self.u, "shopname", 10, "hasAmount", "itemname1", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u, "shopname")
        self.assertEqual(r.res, [[1, "hasAmount", "itemname1", 4, 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_policy(self.u, "shopname", 10, "hasAmount", "itemname2", 2)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u, "shopname")
        self.assertTrue((not r.isexc) and r.res == [[1, "hasAmount", "itemname1", 4, 10],
                                                    [2, "hasAmount", "itemname2", 2, 10]])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertEqual(r.res, [["purchase", 1]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 2)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertEqual(r.res, [["purchase", 1], ["purchase", 2]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.isexc) and r.res == {"shopname": [{"name": "itemname1",
                                                                 "price": 5,
                                                                 "amount": 30,
                                                                 "count": 4,
                                                                 "category": "animal objects",
                                                                 "description": "cats and clocks"}]})
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue(not r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.shopping_carts_add_item(self.u, "itemname2", "shopname", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertEqual(r.res,  {'shopname': [{'name':'itemname1','price': 5.0,'count': 4,'amount': 30,'category':'animal objects','description':'cats and clocks'},
                                              {'name':'itemname2','price': 2.0,'count': 4,'amount': 50,'category':'animal objects','description':'dogs and locks'}]}, r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)

    def testOr(self):
        r = self.m.add_policy(self.u, "shopname", 10, "hasAmount", "itemname1", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u, "shopname")
        self.assertEqual(r.res, [[1, "hasAmount", "itemname1", 4, 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_policy(self.u, "shopname", 10, "hasAmount", "itemname2", 2)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u, "shopname")
        self.assertTrue((not r.isexc) and r.res == [[1, "hasAmount", "itemname1", 4, 10],
                                                    [2, "hasAmount", "itemname2", 2, 10]])
        r = self.m.compose_policy(self.u, "shopname", "or", 1, 2)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u, "shopname")
        self.assertTrue((not r.isexc) and r.res == [[1, "hasAmount", "itemname1", 4, 10],
                                                    [2, "hasAmount", "itemname2", 2, 10], [3, "or", 1, 2]])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 3)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertEqual(r.res, [["purchase", 3]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.isexc) and r.res ==
                        {"shopname": [{"name": "itemname1",
                                      "price": 5,
                                      "amount": 30,
                                      "count": 4,
                                      "category": "animal objects",
                                      "description": "cats and clocks"}]})
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.shopping_carts_add_item(self.u, "itemname2", "shopname", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertEqual(r.res, {'shopname': [{'name':'itemname1','price': 5.0,'count': 4,'amount': 30,'category':'animal objects','description':'cats and clocks'},
                                              {'name':'itemname2','price': 2.0,'count': 4,'amount': 50,'category':'animal objects','description':'dogs and locks'}]}, r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.shopping_carts_delete_item(self.u, "itemname1", "shopname", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertEqual(r.res,{'shopname': [{'name':'itemname2','price': 2.0,'count': 4,'amount': 50,'category':'animal objects','description':'dogs and locks'}]}, r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)

    def testNot(self):
        # shopping bag (for "shopname") does not contain 4 items ith name "itemname1"
        r = self.m.add_policy(self.u, "shopname", 10, "hasAmount", "itemname1", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u, "shopname")
        self.assertEqual(r.res, [[1, "hasAmount", "itemname1", 4, 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.compose_policy(self.u, "shopname", "not", 1)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u, "shopname")
        self.assertEqual(r.res, [[1, "hasAmount", "itemname1", 4, 10], [2, "not", 1]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 2)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertEqual(r.res, [["purchase", 2]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.isexc) and r.res == {"shopname": [{"name": "itemname1",
                                                                 "price": 5,
                                                                 "amount": 30,
                                                                 "count": 4,
                                                                 "category": "animal objects",
                                                                 "description": "cats and clocks"}]})
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue(not r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.shopping_carts_delete_item(self.u, "itemname1", "shopname", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertEqual(r.res, {}, r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.validate_purchase_policy(self.u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)

    def testHasAmountDiscount(self):
        r = self.m.add_policy(self.u, "shopname", 10, "hasAmount", "itemname1", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u, "shopname")
        self.assertEqual(r.res, [[1, "hasAmount", "itemname1", 4, 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertEqual(r.res, [["discount", 1, 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.shopping_carts_check_content(self.u)
        self.assertTrue((not r.isexc) and r.res == {"shopname": [{"name": "itemname1", "price": 5, "amount": 30, "count": 4, "category": "animal objects", "description": "cats and clocks"}]})
        r = self.m.calculate_cart_price(self.u)
        self.assertTrue((not r.isexc) and r.res == 18)  # original price is 4*5=20 with 10% discount is 18

    def testComplicated(self):
        self.m.add_policy(self.u, "shopname", 10, "isItem", "itemname1")
        self.m.add_policy(self.u, "shopname", 20, "isShop")
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue((not r.isexc), r.exc)
        self.m.add_discount_policy_to_shop(self.u, "shopname", 2)
        self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 20)
        r = self.m.calculate_cart_price(self.u)
        self.assertTrue((not r.isexc), r.exc)
        self.assertEqual(r.res, 72, r.res)
        self.m.compose_policy(self.u, "shopname", "add", 1, 2)
        self.m.add_discount_policy_to_shop(self.u, "shopname", 3)
        r = self.m.calculate_cart_price(self.u)

        self.assertEqual(r.res, 50.4, r.res)
        self.assertTrue((not r.isexc), r.exc)
        self.m.shopping_carts_add_item(self.u, "itemname2", "shopname", 10)
        r = self.m.calculate_cart_price(self.u)
        self.assertEqual(r.res, 66.4, r.res)
        self.assertTrue((not r.isexc), r.exc)
        self.m.add_policy(self.u, "shopname", 50, "isItem", "itemname2")
        self.m.add_policy(self.u, "shopname", 0, "hasAmount", "itemname1", 6)
        self.m.compose_policy(self.u, "shopname", "and", 4, 5)
        self.m.add_discount_policy_to_shop(self.u, "shopname", 6)
        r = self.m.calculate_cart_price(self.u)
        self.assertEqual(r.res, 58.4, r.res)
        self.assertTrue((not r.isexc), r.exc)
        self.m.shopping_carts_delete_item(self.u, "itemname1", "shopname", 15)
        r = self.m.calculate_cart_price(self.u)
        self.assertEqual(r.res, 28.6, r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testIsCategory(self):
        self.m.add_policy(self.u, "shopname", 10, "isCategory", "animal objects")
        self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        r = self.m.calculate_cart_price(self.u)
        self.assertTrue((not r.isexc) and r.res == 18)

    def testIsAfterTime(self): # run this test after 10AM
        self.m.add_policy(self.u, "shopname", 10, "isAfterTime", 10, 0)
        self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.m.add_discount_policy_to_shop(self.u, "shopname", 2)
        self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        r = self.m.calculate_cart_price(self.u)
        self.assertTrue((not r.isexc) and r.res == 18)

    def testIsFounder(self):
        self.m.add_policy(self.u, "shopname", 10, "isFounder")
        self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        r = self.m.calculate_cart_price(self.u)
        self.assertTrue((not r.isexc) and r.res == 18)
        self.m.logout(self.u)
        self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        r = self.m.calculate_cart_price(self.u)
        self.assertTrue((not r.isexc) and r.res == 20)

    def testIsOwner(self):
        self.m.add_policy(self.u, "shopname", 10, "isOwner")
        self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        r = self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        r = self.m.calculate_cart_price(self.u)
        self.assertTrue((not r.isexc) and r.res == 20)
        self.m.logout(self.u)
        r = self.m.login_into_the_trading_system(self.u2, "ownername", "password")
        r=self.m.shopping_carts_add_item(self.u2, "itemname1", "shopname", 4)
        self.assertTrue((not r.isexc))
        r = self.m.calculate_cart_price(self.u2)
        self.assertTrue((not r.isexc))
        self.assertEqual(r.res, 18,r.exc)

    def testMax(self):
        self.m.add_policy(self.u, "shopname", 10, "isFounder")
        self.m.add_policy(self.u, "shopname", 20, "isShop")
        r = self.m.compose_policy(self.u, "shopname", "max",  1,2)
        self.m.add_discount_policy_to_shop(self.u, "shopname", 3)
        self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 4)
        r = self.m.calculate_cart_price(self.u)
        self.assertTrue((not r.isexc) and r.res == 16)


if __name__ == '__main__':
    unittest.main()
