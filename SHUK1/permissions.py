class permissions:
    def __init__(self,manager,shop,grantor):
        self.manager = manager
        self.shop = shop
        self.grantor = grantor

        #check association class constraint