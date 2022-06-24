# from .Logger import Logger


from enum import Enum


class Permission(Enum):
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

class PermissionsDTO:
    def __init__(self,assignedPermission):
        self.assignedPermission = assignedPermission  # {PermissionEnum}