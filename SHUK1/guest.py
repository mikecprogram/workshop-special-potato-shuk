import sqlite3

class guest:

    def __init__(self,user):
        self.user=user
    def register(self, marketid, username, password):
        try:
            with sqlite3.connect("market.db") as connection:
                cur =connection.cursor()
                command="INSERT INTO users (market,username,password) VALUES ("+str(marketid)+",\""+str(username)+"\",\""+str(password)+"\");"
                print(command)
                r=cur.execute(command)
                print(r.fetchall())
                connection.commit()              
        except Exception as e:
            print("ERROR:",e)
        finally:
            connection.close()
    def login(self, marketid, username, password):
        try:
            with sqlite3.connect("market.db") as connection:
                cur =connection.cursor()
                command="SELECT * FROM users WHERE market IS "+str(marketid)+" AND username IS \""+str(username)+"\" AND password IS \""+str(password)+"\";"
                print(command)
                r=cur.execute(command)
                if r.fetchall()!=[]:
                    return True
                else:
                    print("bad username or password")
                    return False
                
        except Exception as e:
            print("ERROR:",e)
        finally:
            connection.close()
