from Dev.DAL.objects.DB import *

class AutoIncreamentDal(db.Entity):
    id = PrimaryKey(int,auto=True)


