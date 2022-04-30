from market import *
from user import *
from membersController import *


class testBridge:
    def __init__(self, market):
        self.market = market
        self.controller = market.getController()
        self.test_guest_login_logout()
        self.test_register()
        self.test_create_shop()


    #test II.1.1,II.1.2
    def test_guest_login_logout(self):
        g1 = self.market.enter()

        assert (g1 in self.market.activeUsers), "Oh, guest is not active"
        self.market.exit(g1)

        assert not (g1 in self.market.activeUsers), "Oh, guest is still in market"

    #test II.1.3,II.1.4
    def test_register(self):
        g1 = self.market.enter()
        g1.register("User1", "Pass1")
        assert type(g1._state).__name__ == "guest", "Oh no.. the guest is logged in somehow.."
        g1.login("User1", "Pass1")
        assert type(g1._state).__name__ == "member", "Oh no.. the member is logged out in somehow.."
        g1.logout()
        assert type(g1._state).__name__ == "guest", "Oh no.. the member is still logged in somehow.."

    def test_create_shop(self):
        mem1 = self.market.enter()
        mem1.register("fon", "Passs")
        mem1.login("fon","Passs")
        mem1.openShop("Banana")
        assert mem1._state.foundedShops[0].name == "Banana", "Error no banana found"
    #Loader for tests 2 - member and guest
    def test_2(self):
        mem1 = self.market.enter()
        mem1.register("Use2", "Passs")
        mem1.login("Use2","Passs")
        assert type(mem1._state).__name__ == "member", "Oh no.. the member is logged out in somehow.."
        g1 = self.market.enter()
        assert type(mem1._state).__name__ == "guest", "Oh no.. the member is logged out in somehow.."
        self.test_gather_info_shops_products(mem1)
        self.test_gather_info_shops_products(g1)


    #test II.2.1
    def test_gather_info_shops_products(self,user):
        shopst = self.market.getShops()
        pass

    #test II.2.1
    def test_search_products(self,user):
        # test II.2.1
        pass

    def test_save_products(self, user):
        pass

if __name__ == "__main__":
    testBridge(market())
    print("\u001b[32mEverything passed\u001b[0m")

# m=market()
# u=m.enter()
# u.getShops()
