from Dev.DataLayer.DalObject import DalObject


class DalPolicy(DalObject):

    def __init__(self, percent, shopname, type, ID, name, arg1, arg2):
        self.type = type
        self.shopname = shopname
        self.ID = ID
        self.name = name
        self.arg1 = arg1
        self.arg2 = arg2
        self.percent = percent

    def store(self):
        print("Policy number: " + str(self.ID) + \
              "\npolicy type: " + type(self).__name__ + \
              "\npolicy discount: " + str(self.percent) + \
              "\n")
