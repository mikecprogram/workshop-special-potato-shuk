import unittest
from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.m = SystemService()
        self.m.initialization_of_the_system()
        self.u = self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u, "username", "password")
        # need to login, create shop and add items to it for test
        self.m.login_into_the_trading_system(self.u, "username", "password")
        self.m.shop_open(self.u, "shopname")
        self.m.adding_item_to_the_shops_stock(self.u, "itemname", "shopname", "animal objects", "cats and clocks", 5,
                                              10)
        self.m.adding_item_to_the_shops_stock(self.u, "itemname2", "shopname", "animal objects", "bird bricks", 2, 50)

    # basic policies
    """
    def testIsItem(self):
        r = self.m.add_policy(self.u, 10, "isItem", "itemname")
        self.assertTrue(r.response, r.exc)
        self.assertTrue((not r.is_exception), r.exc)
        r = self.m.get_my_policies(self.u)
        self.assertEqual(r.response, [[1, "isItem", "itemname", 10]], r.res)
        self.assertTrue((not r.is_exception), r.exc)
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue(r.response, r.exc)
        self.assertTrue((not r.is_exception), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertEqual(r.response, [["discount", 1, 10]], r.res)
        self.assertTrue((not r.is_exception), r.exc)


    def testIsCategory(self):
        r = self.m.add_policy(self.u, 10, "isCategory", "animal objects")
        self.assertTrue(r.response, r.exc)
        self.assertTrue((not r.is_exception), r.exc)
        r = self.m.get_my_policies(self.u)
        self.assertEqual(r.response, [[1, "isCategory", "animal objects", 10]], r.res)
        self.assertTrue((not r.is_exception), r.exc)
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue(r.response, r.exc)
        self.assertTrue((not r.is_exception), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["discount", 1, 10]])"""

    def testHasAmountDiscount(self):
        r = self.m.add_policy(self.u, 10, "hasAmount", "itemname", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u)
        self.assertEqual(r.res, [[1, "hasAmount", "itemname", 4, 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertEqual(r.res, [["discount", 1, 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testIsShopDiscount(self):
        r = self.m.add_policy(self.u, 10, "isShop")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u)
        self.assertEqual(r.res, [[1, "isShop", 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertEqual(r.res, [["discount", 1, 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testHasPriceDiscount(self):
        r = self.m.add_policy(self.u, 10, "hasPrice", "itemname", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u)
        self.assertEqual(r.res, [[1, "hasPrice", "itemname", 4, 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertEqual(r.res, [["discount", 1, 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testMulti(self):
        r = self.m.add_policy(self.u, 10, "hasPrice", "itemname", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_policy(self.u, 10, "isItem", "itemname")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u)
        self.assertEqual(r.res, [[1, "hasPrice", "itemname", 4, 10], [2, "isItem", "itemname", 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 2)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertEqual(r.res, [["discount", 1, 10], ["purchase", 2]], r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testNot(self):
        r = self.m.add_policy(self.u, 10, "hasPrice", "itemname", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u)
        self.assertEqual(r.res, [[1, "hasPrice", "itemname", 4, 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.compose_policy(self.u, "not", 1)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u)
        self.assertEqual(r.res, [[1, "hasPrice", "itemname", 4, 10], [2, "not", 1]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 2)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertEqual(r.res, [["purchase", 2]], r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testAnd(self):
        r = self.m.add_policy(self.u, 10, "hasPrice", "itemname", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u)
        self.assertEqual(r.res, [[1, "hasPrice", "itemname", 4, 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_policy(self.u, 10, "isItem", "itemname")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u)
        self.assertEqual(r.res, [[1, "hasPrice", "itemname", 4, 10], [2, "isItem", "itemname", 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.compose_policy(self.u, "and", 1, 2)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u)
        self.assertEqual(r.res, [[1, "hasPrice", "itemname", 4, 10], [2, "isItem", "itemname", 10], [3, "and", 1, 2]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 3)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertEqual(r.res, [["purchase", 3]], r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testOr(self):
        r = self.m.add_policy(self.u, 10, "hasPrice", "itemname", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u)
        self.assertEqual(r.res, [[1, "hasPrice", "itemname", 4, 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_policy(self.u, 10, "isItem", "itemname")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u)
        self.assertEqual(r.res, [[1, "hasPrice", "itemname", 4, 10], [2, "isItem", "itemname", 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.compose_policy(self.u, "or", 1, 2)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u)
        self.assertEqual(r.res, [[1, "hasPrice", "itemname", 4, 10], [2, "isItem", "itemname", 10], [3, "or", 1, 2]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 3)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertEqual(r.res, [["purchase", 3]], r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testXor(self):
        r = self.m.add_policy(self.u, 10, "hasPrice", "itemname", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u)
        self.assertEqual(r.res, [[1, "hasPrice", "itemname", 4, 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_policy(self.u, 10, "isItem", "itemname")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u)
        self.assertEqual(r.res, [[1, "hasPrice", "itemname", 4, 10], [2, "isItem", "itemname", 10]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.compose_policy(self.u, "xor", 1, 2)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u)
        self.assertEqual(r.res, [[1, "hasPrice", "itemname", 4, 10], [2, "isItem", "itemname", 10], [3, "xor", 1, 2]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 3)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertEqual(r.res, [["purchase", 3]], r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testDelete(self):
        r = self.m.add_policy(self.u, 10, "hasPrice", "itemname", 4)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_policy(self.u, 10, "isItem", "itemname")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_my_policies(self.u)
        self.assertEqual(r.res, [[1, "hasPrice", "itemname", 4, 10], [2, "isItem", "itemname", 10]], r.res)
        self.assertTrue(not r.isexc, r.exc)
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 2)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertEqual(r.res, [["discount", 1, 10], ["purchase", 2]], r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.delete_policy(self.u, "shopname", 1)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertEqual(r.res, [["purchase", 2]], r.res)
        self.assertTrue((not r.isexc), r.exc)


if __name__ == '__main__':
    unittest.main()
