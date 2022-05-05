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
        #add to "shopname" 10 "itemname" items. self.u is user identifier for premmisions (if any exist)
        self.m.logout(self.u)
        

        
    def testSearchName(self):
        result=self.m.search("itemname",None,None)
        self.assertTrue(True) #dont know result structure for now just print 
        print(result)
    def testSearchCategory(self):
        result=self.m.search(None,"category",None)
        self.assertTrue(True) #dont know result structure for now just print 
        print(result)
    def testSearchKeyword(self):
        result=self.m.search(None,None,"keyword1")
        self.assertTrue(True) #dont know result structure for now just print 
        print(result)
        
    

    
        
if __name__ == '__main__':
    unittest.main()
