from passlib.hash import argon2

import os

class PasswordHasher:
    def __init__(self, iterator: int = 16, memory: int = 32789):
        self.iterator = iterator
        self.memory = memory

    def gen_salt(self):
        return os.urandom(16) # Use a secure random generator
    
    def hash_password(self, password: str):
        salt = self.gen_salt()
        return argon2.hash(password, salt=salt, iterations=self.iterator, memory=self.memory)
    
    def verify_password(self, password, hashed_password):
        return argon2.verify(password, hashed_password)
    