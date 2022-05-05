import unittest
import sys
#this is how you import from different folder in python:
sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\SHUK1')

from market import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.m=marketService()#new market every test
        self.u=self.m.enter()
        #need to login, create shop and add items to it for test
        self.m.register(self.u,"username","password")
        self.m.login(self.u,"username","password")
        self.m.foundShop(self.u,"shopname")
        self.m.defineItemInShop(self.u,"shopname","itemname","category",["keyword1"])
        self.m.addItemToShop(self.u,"shopname","itemname",10)
        #add to "shopname" 10 "itemname" items. self.u is user identifier for premmisions (if any exist)
        self.m.logout(self.u)
        
               
    def testGoodGuest(self):
        shopInfo=self.m.getShopInfo("shopname")
        itemInfo=self.m.getItemInfo("shopname","itemname")
        self.assertTrue(True) #dont know detail structure for now just print 
        print(shopInfo, itemInfo)
        
    def testGoodMember(self): #in case information is defferent
        self.m.login(self.u,"username","password")
        shopInfo=self.m.getShopInfo("shopname")
        itemInfo=self.m.getItemInfo("shopname","itemname")
        self.assertTrue(True) #dont know detail structure for now just print 
        print(shopInfo, itemInfo)
        
    def testbadShopGuest(self):
        shopInfo=self.m.getShopInfo("badshopname")
        self.assertEqual(shopInfo,None)
        
    def testbadShopMember(self):
        self.m.login(self.u,"username","password")
        shopInfo=self.m.getShopInfo("badshopname")
        self.assertEqual(shopInfo,None)
        
    def testbadItemGuest(self):
        shopInfo=self.m.getShopInfo("shopname")
        itemInfo=self.m.getItemInfo("shopname","baditemname")
        self.assertEqual(itemInfo,None)
        
    def testbadShopMember(self):
        self.m.login(self.u,"username","password")
        shopInfo=self.m.getShopInfo("shopname")
        itemInfo=self.m.getItemInfo("shopname","baditemname")
        self.assertEqual(itemInfo,None)

    
        
if __name__ == '__main__':
    unittest.main()
