# from .Logger import Logger


from enum import Enum


class Permission(Enum):
    StockManaging = 0
    DiscountPolicyChanging = 1
    PurchasePolicyChanging = 2
    ShopOwnerAssigning = 3
    ShopOwnerUnassigning = 4
    ShopManagerAssigning = 5
    ShopManagerUnassigning = 6
    ShopManagerPermissionsChanging = 7
    ShopClosing = 8
    ClosedShopOpening = 9
    UsersQuestionsAnswering = 10
    ShopRolesInfoGetting = 11
    InshopPurchasesHistoryGetting = 12


class Permissions:

    def __init__(self):
        self._assignedPermission = set()  # set of permission.enum
        self.add_permission(Permission.UsersQuestionsAnswering)
        self.add_permission(Permission.InshopPurchasesHistoryGetting)

    def add_permission(self, permission):
        if permission in self._assignedPermission:
            raise Exception('Member already has required permission')
        self._assignedPermission.add(permission)

    def can_manage_stock(self):
        return Permission.StockManaging in self._assignedPermission

    def can_change_discount_policy(self):
        return Permission.DiscountPolicyChanging in self._assignedPermission

    def can_change_purchase_policy(self):
        return Permission.PurchasePolicyChanging in self._assignedPermission

    def can_assign_manager(self):
        return Permission.ShopManagerAssigning in self._assignedPermission

    def can_assign_owner(self):
        return Permission.ShopOwnerAssigning in self._assignedPermission

    def can_unassign_manager(self):
        return Permission.ShopManagerUnassigning in self._assignedPermission

    def can_unassign_owner(self):
        return Permission.ShopOwnerUnassigning in self._assignedPermission

    def can_get_shop_roles_info(self):
        return Permission.ShopRolesInfoGetting in self._assignedPermission

    def can_close_shop(self):
        return Permission.ShopClosing in self._assignedPermission

    def can_get_inshop_purchases_history(self):
        return Permission.InshopPurchasesHistoryGetting in self._assignedPermission

    def can_change_shop_manager_permissions(self):
        return Permission.ShopManagerPermissionsChanging in self._assignedPermission

    def can_open_closed_shop(self):
        return Permission.ClosedShopOpening in self._assignedPermission

    def can_answer_users_questions(self):
        return Permission.UsersQuestionsAnswering in self._assignedPermission