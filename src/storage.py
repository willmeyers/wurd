import sqlite
import datetime


class WurdStorage:
    name = 'My Passwords'
    
    
    def __init__(self):
        self.init_prompt()


    def init_prompt(self):
        print('To begin using Wurd, you must set up a key')
        
