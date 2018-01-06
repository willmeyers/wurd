from tkinter import *


class PasswordPopup(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        
        self.create_widgets()
        self.pack()
        
    def create_widgets(self):
        self.l = Label(self)
        self.l['text'] = 'PASSWORD'
        self.l.config(font=('monospace', 20, 'bold'))
        self.l.pack({'side': 'top'})
        
        self.save_copy = Button(self)
        self.save_copy['text'] = 'Save and Copy'
        self.save_copy['command'] = self.save_password
        self.save_copy.pack({'side':'left'})

        self.discard = Button(self)
        self.discard['text'] = 'Discard'
        self.discard['command'] = self.discard_password
        self.discard.pack({'side':'right'})

    def save_password(self):
        pass


    def discard_password(self):
        pass
