import sqlite3

class guest:

    def __init__(self,user):
        self.user=user
    def register(self, username, password):
        try:
            with sqlite3.connect("market.db") as connection:
                cur =connection.cursor()
                command="INSERT INTO users (username,password) VALUES (\""+str(username)+"\",\""+str(password)+"\");"
                print(command)
                r=cur.execute(command)
                print(r)
                connection.commit()              
        except Exception as e:
            print("ERROR:",e)
        finally:
            connection.close()
    def login(self, username, password):
        try:
            with sqlite3.connect("market.db") as connection:
                cur =connection.cursor()
                command="SELECT * FROM users WHERE  username IS \""+str(username)+"\" AND password IS \""+str(password)+"\";"
                print(command)
                r=cur.execute(command)
                print(r.fetchall())
                if r.fetchall()==[]:
                    return True
                else:
                    print("bad username or password")
                    return False
                
        except Exception as e:
            print("ERROR:",e)
        finally:
            connection.close()
