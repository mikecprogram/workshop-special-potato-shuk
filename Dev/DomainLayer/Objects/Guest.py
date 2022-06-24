##from .Logger import Logger


class Guest:

    def __init__(self, user):
        self._user = user  # is it necessary here ? answer: ?

    def assign_owner(self, shopName, memberToAssign):
        raise Exception("Guest could not assign shop owners!")

    def get_permissions_report(self, shopName, member):
        raise Exception("Guest could not get %s permissions." % member)

    def assign_manager(self, shopNmae, member):
        raise Exception("Guest could not assign shop managers!")

    def openShop(self, shop):
        raise Exception("Guest could not open a shop!")

    def getRolesInfoReport(self, shopName):
        raise Exception("Guest could not do this operation")

    def close_shop(self, shopName):
        raise Exception("Guest could not do this operation")

    def get_inshop_purchases_history(self, shopname):
        raise Exception('Guest could not get in-shop purchases history!')

    def grant_permission(permission_code, shop_name, target_manager):
        raise Exception('Guest could not grant permissions!')

    def withdraw_permission(permission_code, shop_name, target_manager):
        raise Exception('Guest could not withdraw permissions!')
