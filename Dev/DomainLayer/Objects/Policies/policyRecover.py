


class policyRecover:

    @staticmethod
    def Recover(dal): #dont take imports out of the static method!!!!!
        from Dev.DomainLayer.Objects.Policies.policyAdd import policyAdd
        from Dev.DomainLayer.Objects.Policies.policyAnd import policyAnd
        from Dev.DomainLayer.Objects.Policies.policyHasAmount import policyHasAmount
        from Dev.DomainLayer.Objects.Policies.policyHasPrice import policyHasPrice
        from Dev.DomainLayer.Objects.Policies.policyIf import policyIf
        from Dev.DomainLayer.Objects.Policies.policyIsAfterTime import policyIsAfterTime
        from Dev.DomainLayer.Objects.Policies.policyIsCategory import policyIsCategory
        from Dev.DomainLayer.Objects.Policies.policyIsFounder import policyIsFounder
        from Dev.DomainLayer.Objects.Policies.policyIsItem import policyIsItem
        from Dev.DomainLayer.Objects.Policies.policyIsOwner import policyIsOwner
        from Dev.DomainLayer.Objects.Policies.policyIsShop import policyIsShop
        from Dev.DomainLayer.Objects.Policies.policyMax import policyMax
        from Dev.DomainLayer.Objects.Policies.policyNot import policyNot
        from Dev.DomainLayer.Objects.Policies.policyOr import policyOr
        from Dev.DomainLayer.Objects.Policies.policyXor import policyXor
        t = dal.type
        shopname = dal.shopname
        if t == "isShop":
            return policyIsShop(shopname, dal.ID, dal.percent)
        if t == "isFounder":
            return policyIsFounder(shopname, dal.ID, dal.percent)
        if t == "isOwner":
            return policyIsOwner(shopname, dal.ID, dal.percent)
        if t == "isCategory":
            return policyIsCategory(shopname, dal.ID, dal.percent, dal.arg1)
        if t == "isItem":
            return policyIsItem(shopname, dal.ID, dal.percent, dal.arg1)
        if t == "hasAmount":
            return policyHasAmount(shopname, dal.ID, dal.percent, dal.arg1, dal.arg2)
        if t == "hasPrice":
            return policyHasPrice(shopname, dal.ID, dal.percent, dal.arg1, dal.arg2)
        if t == "isAfterTime":
            return policyIsAfterTime(shopname, dal.ID, dal.percent, dal.arg1, dal.arg2)

        if t == "not":
            pt = policyRecover.Recover(dal.arg1)
            return policyNot(shopname, dal.ID, pt)
        if t == "and":
            pt1 = policyRecover.Recover(dal.arg1)
            pt2 = policyRecover.Recover(dal.arg2)
            return policyAnd(shopname, dal.ID, pt1, pt2)
        if t == "or":
            pt1 = policyRecover.Recover(dal.arg1)
            pt2 = policyRecover.Recover(dal.arg2)
            return policyOr(shopname, dal.ID, pt1, pt2)
        if t == "xor":
            pt1 = policyRecover.Recover(dal.arg1)
            pt2 = policyRecover.Recover(dal.arg2)
            return policyXor(shopname, dal.ID, pt1, pt2)
        if t == "if":
            pt1 = policyRecover.Recover(dal.arg1)
            pt2 = policyRecover.Recover(dal.arg2)
            return policyIf(shopname, dal.ID, pt1, pt2)
        if t == "add":
            pt1 = policyRecover.Recover(dal.arg1)
            pt2 = policyRecover.Recover(dal.arg2)
            return policyAdd(shopname, dal.ID, pt1, pt2)
        if t == "max":
            pt1 = policyRecover.Recover(dal.arg1)
            pt2 = policyRecover.Recover(dal.arg2)
            return policyMax(shopname, dal.ID, pt1, pt2)