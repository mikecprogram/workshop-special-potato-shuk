import unittest
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
        self.m.adding_item_to_the_shops_stock(self.u, "itemname", "shopname", "animal objects", "cats and clocks", 5,
                                              10)
        self.m.adding_item_to_the_shops_stock(self.u, "itemname2", "shopname", "animal objects", "bird bricks", 2, 50)

    # basic policies
    def testIsItem(self):
        r = self.m.add_policy(self.u, 10, "isItem", "itemname")
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "isItem", "itemname", 10]])
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["discount", 1]])
        r = self.m.get_item_policies(self.u, "shopname", "itemname")
        self.assertTrue((not r.is_exception) and r.response == [["discount", 1]])

    def testIsCategory(self):
        r = self.m.add_policy(self.u, 10, "isCategory", "animal objects")
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "isCategory", "animal objects", 10]])
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["discount", 1]])
        r = self.m.get_item_policies(self.u, "shopname", "itemname")
        self.assertTrue((not r.is_exception) and r.response == [["discount", 1]])

    def testHasAmountDiscount(self):
        r = self.m.add_policy(self.u, 10, "hasAmount", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasAmount", 4, 10]])
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["discount", 1]])
        r = self.m.get_item_policies(self.u, "shopname", "itemname")
        self.assertTrue((not r.is_exception) and r.response == [["discount", 1]])

    def testIsShopDiscount(self):
        r = self.m.add_policy(self.u, 10, "isShop")
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "isShop", 10]])
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["discount", 1]])
        r = self.m.get_item_policies(self.u, "shopname", "itemname")
        self.assertTrue((not r.is_exception) and r.response == [["discount", 1]])

    def testHasRawPriceDiscount(self):
        r = self.m.add_policy(self.u, 10, "hasPrice", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasPrice", 4, 10]])
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["discount", 1]])
        r = self.m.get_item_policies(self.u, "shopname", "itemname")
        self.assertTrue((not r.is_exception) and r.response == [["discount", 1]])

    def testMulti(self):
        r = self.m.add_policy(self.u, 10, "hasPrice", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.add_policy(self.u, 10, "isItem", "itemname")
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasPrice", 4, 10], [2, "isItem", "itemname", 10]])
        r = self.m.add_discount_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 2)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["discount", 1], ["purchase", 2]])
        r = self.m.get_item_policies(self.u, "shopname", "itemname")
        self.assertTrue((not r.is_exception) and r.response == [["discount", 1], ["purchase", 2]])
        r = self.m.get_item_policies(self.u, "shopname", "itemname2")
        self.assertTrue((not r.is_exception) and r.response == [["discount", 1]])

    def testNot(self):
        r = self.m.add_policy(self.u, 10, "hasPrice", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasPrice", 4, 10]])
        r = self.m.compose_policy(self.u, "not", 1)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasPrice", 4, 10], [2, "not", 1]])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 2)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 2]])
        r = self.m.get_item_policies(self.u, "shopname", "itemname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 2]])

    def testAnd(self):
        r = self.m.add_policy(self.u, 10, "hasPrice", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasPrice", 4, 10]])
        r = self.m.add_policy(self.u, 10, "isItem", "itemname")
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasPrice", 4, 10], [2, "isItem", "itemname", 10]])
        r = self.m.compose_policy(self.u, "and", 1, 2)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue(
            (not r.is_exception) and r.response == [[1, "hasPrice", 4, 10], [2, "isItem", "itemname", 10], [3, "and", 1, 2]])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 3)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 3]])
        r = self.m.get_item_policies(self.u, "shopname", "itemname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 3]])

    def testOr(self):
        r = self.m.add_policy(self.u, 10, "hasPrice", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasPrice", 4, 10]])
        r = self.m.add_policy(self.u, 10, "isItem", "itemname")
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasPrice", 4, 10], [2, "isItem", "itemname", 10]])
        r = self.m.compose_policy(self.u, "or", 1, 2)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue(
            (not r.is_exception) and r.response == [[1, "hasPrice", 4, 10], [2, "isItem", "itemname", 10], [3, "or", 1, 2]])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 3)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 3]])
        r = self.m.get_item_policies(self.u, "shopname", "itemname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 3]])

    def testXor(self):
        r = self.m.add_policy(self.u, 10, "hasPrice", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasPrice", 4, 10]])
        r = self.m.add_policy(self.u, 10, "isItem", "itemname")
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasPrice", 4, 10], [2, "isItem", "itemname", 10]])
        r = self.m.compose_policy(self.u, "xor", 1, 2)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue(
            (not r.is_exception) and r.response == [[1, "hasPrice", 4, 10], [2, "isItem", "itemname", 10], [3, "xor", 1, 2]])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 3)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 3]])
        r = self.m.get_item_policies(self.u, "shopname", "itemname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 3]])

    # NEED TO ADD TESTS FOR DELETE AND EDIT POLICIES


if __name__ == '__main__':
    unittest.main()
