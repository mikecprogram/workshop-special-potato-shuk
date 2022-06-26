
import sqlite3

class DB(): #singleton
    addr = "ShukDb.db"
    inst = None #static

    def __init__(self, addr):
        self.addr = addr

    def connect(self):
        return sqlite3.connect(self.addr)

    @staticmethod
    def getDB():
        if DB.inst is None:
            DB.inst = DB(DB.addr)
        return DB.inst