class membersController:
    def __init__(self,market):
        self.market=market
        self.members=[] #initialize (load) member list
        self.passwords = []
    def register(self,username,password):
        if(username in self.members):
            print("User " + username + "is already defined")
            return False
        else:
            self.members.append(username)
            self.passwords[username] = password
            return True


    def login(self,username,password):
        if (username in self.members):
            if(self.passwords[username] == password):
                return True
            else:
                return False
        else:
            return False