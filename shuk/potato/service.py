import SystemService
class Service():
    def __init__(self,notifyPlugin ) -> None:
        self.m = SystemService()
        response = self.m.initialization_of_the_system()
        if response.isexc:
            print("BUG:")
            print(response.exc)
        self.notifyPlugin = notifyPlugin
        #initiate service layer
        print("created")
        pass
    def exit(self,token):
        pass
    def enter(self):
        token = self.m.get_into_the_Trading_system_as_a_guest()
        if response.isexc:
            print("BUG:")
            print(response.exc)
        token = token.res
        return token
    def getUserStatus(self):
        return "Mike"
    def login(self, token,username):
        return "False!"
    def register(self, token,username):
        response = self.m.registration_for_the_trading_system(self.u,"username","password")
        
        return "False!"