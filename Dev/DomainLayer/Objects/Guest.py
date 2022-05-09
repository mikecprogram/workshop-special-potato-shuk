from .Logger import Logger
from .Member import Member

class Guest:

    def ___init___(self, user):
        self._user = user
        
   
    def logout(self):
        #should do nothing on logout by definition
        pass


    def login(self, marketid, username, password):
        pass
    def get_username(self):
        return self._username