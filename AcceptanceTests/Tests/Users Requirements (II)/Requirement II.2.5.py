import unittest
import sys
#this is how you import from different folder in python:
sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\SHUK1')

from market import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.m=marketService()
        self.u=self.m.enter()
        #need to login, create shop and add items to it for test
        self.m.register(self.u,"username","password")
        self.m.login(self.u,"username","password")
        s=self.m.foundShop(self.u,"shopname")
        self.m.defineItemInShop(self.u,"shopname","itemname","category",["keyword1","keyword2"])
        self.m.addItemToShop(self.u,"shopname","itemname",10)
        self.m.defineItemInShop(self.u,"shopname","itemname2","category",["keyword1","keyword3"])
        self.m.addItemToShop(self.u,"shopname","itemname",10)
        #add to "shopname" 10 "itemname" items. self.u is user identifier for premmisions (if any exist)
        self.m.logout(self.u)
        

        
    def testPayment(self):
        self.assertTrue(True) 
        
        
    
    
        
if __name__ == '__main__':
    unittest.main()
