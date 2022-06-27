from Dev.DAL.objects.AssignmentDAL import db
from Dev.DAL.objects.imports import *
from os.path import exists

def initializeDatabase(provider='sqlite', filename='database.db'):
    print(exists(filename))
    if exists(filename):
        db.bind(provider=provider, filename=filename, create_db=False)
        db.generate_mapping(create_tables=False)
    else:
        db.bind(provider=provider, filename=filename, create_db=True)
        db.generate_mapping(create_tables=True)


