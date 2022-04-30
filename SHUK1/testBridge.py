from market import *
from user import *
from membersController import *


class testBridge:
    def __init__(self, market):
        self.market = market
        self.controller = market.getController()
        self.test_guest_login_logout()
        self.test_register()


    #test II.1.1,II.1.2
    def test_guest_login_logout(self):
        g1 = self.market.enter()

        assert (g1 in self.market.activeUsers), "Oh, guest is not active"
        self.market.exit(g1)

        assert not (g1 in self.market.activeUsers), "Oh, guest is still in market"

    #test II.1.3
    def test_register(self):
        g1 = self.market.enter()
        g1.register("User1", "Pass1")
        print(type(g1._state).__name__ )
        assert type(g1._state).__name__ == "guest", "Oh no.. the guest is logged in somehow.."
        g1.login("User1", "Pass1")
        assert type(g1._state).__name__ == "member", "Oh no.. the member is logged out in somehow.."
        g1.logout()
        assert type(g1._state).__name__ == "guest", "Oh no.. the member is still logged in somehow.."



if __name__ == "__main__":
    testBridge(market())
    print("\u001b[32mEverything passed\u001b[0m")

# m=market()
# u=m.enter()
# u.getShops()
