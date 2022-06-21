import unittest

from Dev.ServiceLayer.SystemService import *

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.m=SystemService()
        self.m.initialization_of_the_system()
        self.u=self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u,"username","password")
        #need to login, create shop and add items to it for test
        self.m.login_into_the_trading_system(self.u,"username","password")
        self.m.shop_open(self.u,"shopname")
        self.m.adding_item_to_the_shops_stock(self.u,"itemname1","shopname","animal objects","cats and clocks",5,10)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname2","shopname","animal objects","dogs and locks",2,50)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname3","rockshop","rocks","rock collection",1,5)
        self.m.logout(self.u)
        

        
    def testSaveCartItemsGood(self):
        r=self.m.shopping_carts_add_item(self.u,"itemname1","shopname",1)

        self.assertTrue((not r.isexc) and r.res ,r.exc)
        
    def testSaveCartBadName(self):
        r=self.m.shopping_carts_add_item(self.u,"baditemname1","shopname",1)
        self.assertTrue(r.isexc)
        
    def testSaveCartBadShop(self):
        r=self.m.shopping_carts_add_item(self.u,"itemname1","badshopname",1)
        self.assertTrue(r.isexc)

    def testSaveCartBadAmount(self):
        r=self.m.shopping_carts_add_item(self.u,"itemname1","shopname",100)
        self.assertTrue(r.isexc)
        
        
        
    
    
        
if __name__ == '__main__':
    unittest.main()
