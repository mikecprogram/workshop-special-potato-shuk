class Composable:  # any basic discount inherits from Composable (isCategory, isMember, hasAmount...)

    def __init__(self, ID, percent):
        self.ID = 0
        self.percent = 0

    def apply(self, user, item):
        pass

    def getDiscount(self):
        return self.percent

    def getID(self):
        return self.ID
