

class DB(): #singleton
    addr = None #static

    @staticmethod
    def getDB():
        return DB.addr

    @staticmethod
    def getDB(addr):
        if DB.addr is None:
            DB.addr = addr
        return DB.addr