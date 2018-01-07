import random


class Password:
    allowed = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-+_=,.<>?:;{}[]~'
    
    def __init__(self, name):
        self.name = name

    def generate(self):
        p = []
        for c in range(16):
            p.append(random.choice(self.allowed))
            random.shuffle(p)

        return ''.join(p)
        
