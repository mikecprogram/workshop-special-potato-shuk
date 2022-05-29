from atexit import register
import threading
from time import sleep
from Market import Market
def logintests():
    timeout = 10
    m = Market(None,None,None,None,timeout)
    t1 = successEnter(m)
    exitTest(m,t1)
    t2 = successEnter(m)
    registertest(m)
    memeberregistertests(m)
    logoutregistertests(m)
    failEnter(m)
    timeoutEnter(m,timeout+1)
def test1():
    m = Market(None,None,None,None,10)
    t1 = m.enter()
    m.register(t1,"FANTA","12345678")
    m.login(t1,"FANTA","12345678")
    m.addToCart(t1,0 ,"Shop1",1)
    m.addToCart(t1,1 ,"Shop1",4)
    print(m.getCartContents(t1))
    m.logout(t1)
    m.addToCart(t1,1 ,"Shop1",5)
    print(m.getCartContents(t1))
    if(m.purchase(t1)):
        print("success!")
    else:
        print("fail")
    
    print(m.getCartContents(t1))
def test2():
    m = Market(None,None,None,None,10)
    t1 = m.enter()
    m.register(t1,"MOK","12345678")
    m.login(t1,"MOK","12345678")
    m.addToCart(t1,0 ,"Shop1",1)
    m.addToCart(t1,1 ,"Shop1",4)
    print(m.getCartContents(t1))
    m.logout(t1)
    m.login(t1,"MOK","12345678")
    m.addToCart(t1,1 ,"Shop1",5)
    print(m.getCartContents(t1))
    if(m.purchase(t1)):
        print("success!")
    else:
        print("fail")
    
    print(m.getCartContents(t1))


def logoutregistertests(m):
    t = m.enter()
    if(m.register(t,"FANTA","12345678")):
        print("Register Success")
        if(m.login(t,"FANTA","12345678")):
            print("Login Success")
        else:
            print("Login Failed")
        m.logout(t)
        try:
            m.register(t,"RAMP","BLOBSBLOBS")
            print("memeberregistertests Success")
        except Exception:
            print("memeberregistertests Failed")
    else:
        print("Register Fail")
def memeberregistertests(m):
    t = m.enter()
    if(m.register(t,"FRICK","EFEFIIJIJ")):
        print("Register Success")
        if(m.login(t,"FRICK","EFEFIIJIJ")):
            print("Login Success")
        else:
            print("Login Failed")
        
        try:
            m.register(t,"MOOK","BLOBSBLOBS")
            print("memeberregistertests Failed")
        except Exception:
            print("memeberregistertests Success")
    else:
        print("Register Fail")
def registertest(m):
    t = m.enter()
    if(m.register(t,"Mike","Password1")):
        print("Register Success")
        if(m.login(t,"Mike","Password1")):
            print("Login Success")
        else:
            print("Login Failed")
        
        try:
            m.logout(t)
            print("Logout Success")
        except Exception:
            print("Logout Failed")
        try:
            m.logout(t)
            print("Logout Failed")
        except Exception:
            print("Logout Success")
    else:
        print("Register Fail")


def exitTest(m,t):
    m.exit(t)
    if(m.isToken(t)):
        raise Exception("exitTest FAIL")
    else:
        print("exitTest Sucess")

def registerTest_(m,t):
    m.register(t,"Mike","Password")
    if(m.isToken(t)):
        raise Exception("exitTest FAIL")
    else:
        print("exitTest Sucess")

def successEnter(m):
    t1 = m.enter()
    if(m.isToken(t1)):
        print("successLogin Sucess")
    else:
        raise Exception("failEnter FAIL")
    return t1
def failEnter(m):
    t1 = 80
    if(m.isToken(t1)):
        raise Exception("failEnter FAIL")
    else:
        print("failEnter Sucess")

def timeoutEnter(m,time):
    t1 = m.enter()
    sleep(time)
    if(m.isToken(t1)):
        raise Exception("timeoutEnter FAIL")
    else:
        print("timeoutEnter Sucess")
if __name__ == '__main__':
    t1 = threading.Thread(target=test1)
    t2 = threading.Thread(target=test2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    test1()