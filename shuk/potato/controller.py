class Controller():
    def __init__(self,notifyPlugin ) -> None:
        self.notifyPlugin = notifyPlugin
        #initiate service layer
        print("created")
        self.token = 0
        pass
    def exit(self,token):
        pass
    def enter(self):
        t = self.token
        self.token = self.token+1
        return t
    def getUserStatus(self):
        return "Mike"
    def login(self, token,username):
        return "False!"