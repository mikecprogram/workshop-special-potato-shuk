
class ShopDTO:

    def __init__(self, shop_name= None,stock= None,is_open= None,founder= None,owners= None,\
                 managers= None,owners_assignments= None,managers_assignments= None,purchases_history= None):
        self.name = shop_name
        self.stock = stock
        self.is_open = is_open  # need to confirm if we need shop's status such as closed/open. TODO
        self.founder = founder
        self.owners = owners  # {ownerUsername, Member} (ò_ó)!!!!!!!!!!!!!!!!!
        self.managers = managers  # {managerUsername, Member}
        #self.purchasePolicies = purchasePolicies
        #self.discountPolicies = discountPolicies
        self.owners_assignments = owners_assignments
        self.managers_assignments = managers_assignments
        self.purchases_history = purchases_history

