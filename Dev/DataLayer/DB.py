import sqlite3


class DB():  # singleton
    addr = "ShukDb.db"
    inst = None  # static

    @staticmethod
    def getDB():
        if DB.inst is None:
            DB.inst = DB(DB.addr)
        return DB.inst

    def __init__(self, addr):
        self.addr = addr

    def loadSystem(self):
        self.initSystem()
        self.loadFromDB()

    def loadFromDB(self):
        pass

    def initSystem(self):
        con = sqlite3.connect(self.addr)
        cur = con.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS "member" (
                    "username"	TEXT NOT NULL UNIQUE,
                    "pass"	TEXT NOT NULL,
                    "age"	INTEGER NOT NULL,
                    PRIMARY KEY("username")
                    );
                    """)
        cur.execute("""CREATE TABLE IF NOT EXISTS "shop" (
                    "shopname"	TEXT NOT NULL UNIQUE,
                    "founder"	TEXT NOT NULL,
                    "isOpen"	INTEGER NOT NULL,
                    PRIMARY KEY("shopname"),
                    FOREIGN KEY("founder") REFERENCES "member"("username")
                    );
                    """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS "stockItem" (
                    "shopname"	TEXT NOT NULL,
                    "ID"	INTEGER NOT NULL,
                    "itemname"	TEXT NOT NULL,
                    "category"	TEXT NOT NULL,
                    "description"	TEXT NOT NULL,
                    "price"	REAL NOT NULL,
                    "count"	INTEGER NOT NULL,
                    PRIMARY KEY("shopname","ID"),
                    FOREIGN KEY("shopname") REFERENCES "shop"("shopname")
                    );
                    """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS "policy" (
                    "shopname"	TEXT NOT NULL,
                    "ID"	INTEGER NOT NULL,
                    "type"	TEXT NOT NULL,
                    "name"	TEXT NOT NULL,
                    "percent"	INTEGER NOT NULL,
                    "arg1"	TEXT,
                    "arg2"	TEXT,
                    FOREIGN KEY("shopname") REFERENCES "shop"("shopname"),
                    PRIMARY KEY("shopname","ID","type")
                    );
                    """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS "basketItem" (
                    "username"	TEXT NOT NULL,
                    "shopname"	TEXT NOT NULL,
                    "itemname"	TEXT NOT NULL,
                    "count"	INTEGER NOT NULL,
                    FOREIGN KEY("itemname") REFERENCES "stockItem"("itemname"),
                    FOREIGN KEY("username") REFERENCES "member"("username"),
                    PRIMARY KEY("username","shopname","itemname"),
                    FOREIGN KEY("shopname") REFERENCES "shop"("shopname")
                    );
                    """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS "assingment" (
                    "role"	TEXT NOT NULL,
                    "shopname"	TEXT NOT NULL,
                    "assignee"	TEXT NOT NULL,
                    "assigner"	TEXT NOT NULL,
                    PRIMARY KEY("role","shopname","assignee"),
                    FOREIGN KEY("assignee") REFERENCES "member"("username"),
                    FOREIGN KEY("shopname") REFERENCES "shop"("shopname"),
                    FOREIGN KEY("assigner") REFERENCES "member"("username")
                    );
                    """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS "permission" (
                    "username"	TEXT NOT NULL,
                    "shopname"	TEXT NOT NULL,
                    "permissions"	TEXT NOT NULL,
                    FOREIGN KEY("username") REFERENCES "member"("username"),
                    PRIMARY KEY("username","shopname"),
                    FOREIGN KEY("shopname") REFERENCES "shop"("shopname")
                    );
                    """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS "notification" (
                    "username"	TEXT NOT NULL,
                    "notification"	TEXT NOT NULL,
                    FOREIGN KEY("username") REFERENCES "member"("username"),
                    PRIMARY KEY("username","notification")
                    );
                    """)
        con.commit()
        con.close()
