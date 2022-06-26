from AssignmentDAL import db
from imports import *
def initializeDatabase():
    db.bind(provider='sqlite', filename='database.db', create_db=True)
    print(db.generate_mapping(create_tables=True))


if __name__ == "__main__":
    initializeDatabase()