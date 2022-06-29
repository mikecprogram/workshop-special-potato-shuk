from Dev.DomainLayer.Objects.Policies.policyIsMember import policyIsMember

dic ={

}

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
        from Dev.DomainLayer.Objects.Policies.policyIsAge import policyIsAge
        t = dal.name
        shopname = dal.shopname
        if t == "policyIsAge":
            return policyIsAge(dal.ID, dal.percent, dal.arg1)
        if t == "policyIsShop":
            return policyIsShop( dal.ID, dal.percent)
        if t == "policyIsFounder":
            return policyIsFounder( dal.ID, dal.percent)
        if t == "policyIsMember":
            return policyIsMember( dal.ID, dal.percent)
        if t == "policyIsOwner":
            return policyIsOwner( dal.ID, dal.percent)
        if t == "policyIsCategory":
            return policyIsCategory( dal.ID, dal.percent, dal.arg1)
        if t == "policyIsItem":
            return policyIsItem( dal.ID, dal.percent, dal.arg1)
        if t == "policyHasAmount":
            return policyHasAmount( dal.ID, dal.percent, dal.arg1, int(dal.arg2))
        if t == "policyHasPrice":
            return policyHasPrice( dal.ID, dal.percent, dal.arg1, float(dal.arg2))
        if t == "policyIsAfterTime":
            return policyIsAfterTime( dal.ID, dal.percent, int(dal.arg1), int(dal.arg2))

        if t == "policyNot":
            pt = policyRecover.Recover(dal.arg1)
            return policyNot( dal.ID, pt)
        if t == "policyAnd":
            pt1 = policyRecover.Recover(dal.arg1)
            pt2 = policyRecover.Recover(dal.arg2)
            return policyAnd( dal.ID, pt1, pt2)
        if t == "policyOr":
            pt1 = policyRecover.Recover(dal.arg1)
            pt2 = policyRecover.Recover(dal.arg2)
            return policyOr( dal.ID, pt1, pt2)
        if t == "policyXor":
            pt1 = policyRecover.Recover(dal.arg1)
            pt2 = policyRecover.Recover(dal.arg2)
            return policyXor( dal.ID, pt1, pt2)
        if t == "policyIf":
            pt1 = policyRecover.Recover(dal.arg1)
            pt2 = policyRecover.Recover(dal.arg2)
            return policyIf( dal.ID, pt1, pt2)
        if t == "policyAdd":
            pt1 = policyRecover.Recover(dal.arg1)
            pt2 = policyRecover.Recover(dal.arg2)
            return policyAdd( dal.ID, pt1, pt2)
        if t == "policyMax":
            pt1 = policyRecover.Recover(dal.arg1)
            pt2 = policyRecover.Recover(dal.arg2)
            return policyMax( dal.ID, pt1, pt2)