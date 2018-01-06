import bcrypt
import string
import random


class Password:
    allowed = string.ascii_letters + string.digits + '!@#$%^&*()-+_=,.<>?:;{}[]~'
    
    def __init__(self, name, dest):
        self.name = name
        self.dest = dest

    def generate(self):
        p = []
        for c in range(16):
            p.append(random.choice(self.allowed))
            random.shuffle(p)

        return ''.join(p)

    def hash(self, password):
        return bcrypt.hashpw(password, bcrypt.gensalt())

        
