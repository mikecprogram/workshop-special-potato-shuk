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


def is_valid_permission(permission_id):
    for permission in Permission:
        if permission.value == permission_id:
            return True
    return False


class Permissions:

    def __init__(self):
        self._assignedPermission = set()  # {PermissionEnum}
        self.add_permission(Permission.UsersQuestionsAnswering)
        self.add_permission(Permission.InshopPurchasesHistoryGetting)

    def has_permission(self, permission):
        return permission in self._assignedPermission

    def add_permission(self, permission_id):
        if not is_valid_permission(permission_id):
            raise Exception('Non valid permission id!')
        permission = Permission(permission_id)
        if self.has_permission(permission):
            raise Exception('Member already has required permission')
        else:
            self._assignedPermission.add(permission)

    def remove_permission(self, permission_id):
        if not is_valid_permission(permission_id):
            raise Exception('Non valid permission id!')
        permission = Permission(permission_id)
        if not self.has_permission(permission):
            raise Exception('Member does not have the required permission')
        else:
            self._assignedPermission.remove(permission)

    def can_manage_stock(self):
        return self.has_permission(Permission.StockManaging)

    def can_change_discount_policy(self):
        return self.has_permission(Permission.DiscountPolicyChanging)

    def can_change_purchase_policy(self):
        return self.has_permission(Permission.PurchasePolicyChanging)

    def can_assign_manager(self):
        return self.has_permission(Permission.ShopManagerAssigning)

    def can_assign_owner(self):
        return self.has_permission(Permission.ShopOwnerAssigning)

    def can_unassign_manager(self):
        return self.has_permission(Permission.ShopManagerUnassigning)

    def can_unassign_owner(self):
        return self.has_permission(Permission.ShopOwnerUnassigning)

    def can_get_shop_roles_info(self):
        return self.has_permission(Permission.ShopRolesInfoGetting)

    def can_close_shop(self):
        return self.has_permission(Permission.ShopClosing)

    def can_get_inshop_purchases_history(self):
        return self.has_permission(Permission.InshopPurchasesHistoryGetting)

    def can_change_shop_manager_permissions(self):
        return self.has_permission(Permission.ShopManagerPermissionsChanging)

    def can_open_closed_shop(self):
        return self.has_permission(Permission.ClosedShopOpening)

    def can_answer_users_questions(self):
        return self.has_permission(Permission.UsersQuestionsAnswering)
