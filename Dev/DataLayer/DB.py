

class DB(): #singleton
    addr = ""
    inst = None #static

    def __init__(self, addr):
        pass

    @staticmethod
    def getDB():
        return DB.inst

    @staticmethod
    def getDB(addr):
        if DB.inst is None:
            DB.inst = DB(addr)
        return DB.inst