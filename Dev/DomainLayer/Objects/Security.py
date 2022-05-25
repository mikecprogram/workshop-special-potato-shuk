import hashlib

class Security():
    def __init__(self):
        pass
    
    def hash(self,password):
        hash_object = hashlib.md5(password.encode())
        return hash_object.hexdigest()