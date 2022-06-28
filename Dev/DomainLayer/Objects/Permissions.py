# from .Logger import Logger


from enum import Enum


class Permission(Enum):
    manager = -1
    StockManaging = 1
    DiscountPolicyChanging = 2
    PurchasePolicyChanging = 3
    ShopOwnerAssigning = 4
    ShopOwnerUnassigning = 5
    ShopManagerAssigning = 6
    ShopManagerUnassigning = 7
    ShopManagerPermissionsChanging = 8
    ShopClosing = 9
    ClosedShopOpening = 10
    UsersQuestionsAnswering = 11
    ShopRolesInfoGetting = 12
    InshopPurchasesHistoryGetting = 13


def is_valid_permission(permission_id):
    for permission in Permission:
        if permission.value == permission_id:
            return True
    return False


class Permissions:

    def __init__(self,assignedPermissions=None):
        if assignedPermissions is None:
            self._assignedPermission = set()  # {PermissionEnum}
            self.add_permission(Permission.UsersQuestionsAnswering.value)
            self.add_permission(Permission.InshopPurchasesHistoryGetting.value)
        else:
            self._assignedPermission=set([Permission(p) for p in assignedPermissions])


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

    def get_permission_report_json(self):
        return {Permission.StockManaging.value: self.can_manage_stock(),
                Permission.DiscountPolicyChanging.value: self.can_change_discount_policy(),
                Permission.PurchasePolicyChanging.value: self.can_change_purchase_policy(),
                Permission.ShopOwnerAssigning.value: self.can_assign_owner(),
                Permission.ShopOwnerUnassigning.value: self.can_unassign_owner(),
                Permission.ShopManagerAssigning.value: self.can_assign_manager(),
                Permission.ShopManagerUnassigning.value: self.can_unassign_manager(),
                Permission.ShopManagerPermissionsChanging.value: self.can_change_shop_manager_permissions(),
                Permission.ShopClosing.value: self.can_close_shop(),
                Permission.ClosedShopOpening.value: self.can_open_closed_shop(),
                Permission.UsersQuestionsAnswering.value: self.can_get_shop_roles_info(),
                Permission.ShopRolesInfoGetting.value: self.can_answer_users_questions(),
                Permission.InshopPurchasesHistoryGetting.value: self.can_get_inshop_purchases_history()}

    """def get_permission_report_json(self):
        return {"Can manage stock":self.can_manage_stock(),
                "Can manage discounts":self.can_change_discount_policy(),
                "Can manage purchase policies":self.can_change_purchase_policy(),
                "Can assign new owners":self.can_assign_owner(),
                "Can remove existing owners":self.can_unassign_owner(),
                "Can assign new managers":self.can_assign_manager(),
                "Can remove existing managers":self.can_unassign_manager(),
                "Can change managers' permissions": self.can_change_shop_manager_permissions(),
                "Can close the shop": self.can_close_shop(),
                "Can reopen the shop if closed": self.can_open_closed_shop(),
                "Can request info about other's permissions":self.can_get_shop_roles_info(),
                "Can reply to shop's users":self.can_answer_users_questions(),
                "Can request shop's purchase history":self.can_get_inshop_purchases_history()}"""
