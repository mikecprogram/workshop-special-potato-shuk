import sqlite3

from shop import shop

class member:
    def __init__(self,user ,username,market = None):
        self.user = user
        self.ownedShops = []#load
        self.foundedShops = []#load
        self.managedShops = []#load
        self.permissions = []#load
        self.assignees = []
        self.admin = market
        self.username=username
        self.load()
        
    def load(self):
        try:
            with sqlite3.connect("market.db") as connection:
                cur =connection.cursor()
                
                command="SELECT name FROM shops WHERE market IS " + str(self.user.market.id) + " AND founder IS \"" + str(self.username) + "\";"
                print(command)
                r=cur.execute(command)
                print(r.fetchall())
                for row in r:
                    self.foundedShops.append(shop(self.user.market.id, row[0], self.username))

                #this is for owners which is not for V1
                """    
                command="SELECT shop FROM shopOwners WHERE market IS "+str(user._market.id)+" AND name IS \""+str(username)+"\";"
                print(command)
                r=cur.execute(command)
                print(r.fetchall())
                for row in r:
                    self.ownedShops.append(shop(user._market.id,row[0],username))
                """
                
        except Exception as e:
            print("ERROR:",e)
        finally:
            connection.close()
        
    def logout(self): #logout not robust!
        try:
            with sqlite3.connect("market.db") as connection:
                cur =connection.cursor()
                for s in self.foundedShops:    
                    command="INSERT INTO shops (market,name,founder) VALUES (" + str(self.user.market.id) + ",\"" + str(s) + "\",\"" + str(self.username) + "\");"
                    print(command)
                    r=cur.execute(command)
                connection.commit()              
        except Exception as e:
            print("ERROR:",e)
        finally:
            connection.close()

    def openShop(self,name):
        shopp = shop(self.user.market.id, name, self.username)
        if(self.user.market.addShop(shopp)):
            self.foundedShops.append(shopp)



    

