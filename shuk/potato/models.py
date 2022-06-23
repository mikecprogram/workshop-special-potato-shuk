# Create your models here
class StockItem():
    def __init__(self, ID, category, name, description, count, purchasepolicy, discountpolicy, price):
        self.id = ID
        self.category = category
        self.desc = description
        self.purchasePolicy = []
        self.discountPolicy = []
        self.name = name
        self.count = count
        self.price = price


class ItemInBasket():
    def __init__(self, ID, category, name, description, count, discountedPrice, fullPrice, quantity):
        self.id = ID
        self.category = category
        self.desc = description
        self.name = name
        self.count = count
        self.discountedPrice = discountedPrice
        self.fullPrice = fullPrice
        self.quantity = quantity


class Shop():
    def __init__(self, id, name, status, founder, owners, managers, purchases_history):
        self.id = id
        self.name = name
        self.status = status
        self.founder = founder
        self.owners = owners
        self.managers = managers
        self.purchases_history = purchases_history


class MemberWithPermissions():
    def __init__(self, id, name, status, founder, owners, managers, purchases_history):
        self.id = id
        self.name = name
        self.status = status
        self.founder = founder
        self.owners = owners
        self.managers = managers
        self.purchases_history = purchases_history


class Policy(): #dumb struct
    def __init__(self, id, name, args, discount):
        self.id = id
        self.name = name
        self.args = args
        self.discount = discount

class TemplatePolicy():
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.demoargs = [(args[i],i) for i in range(len(args))]
