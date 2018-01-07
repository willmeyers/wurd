from tkinter import *
from password import Password


class PasswordPopup(Frame):
    def __init__(self, name, master=None):
        Frame.__init__(self, master)

        self.name = name
        self.password = Password(name).generate()
        
        self.create_widgets()
        self.pack()
        
    def create_widgets(self):
        self.title = Label(self)
        self.title['text'] = self.name.upper()
        self.title.config(font=('Serif', 16, 'bold'))
        self.title.pack({'side': 'top'})
        
        self.plabel = Label(self)
        self.plabel['text'] = self.password
        self.plabel.config(font='TkFixedFont')
        self.plabel.pack({'side': 'top'})
        
        self.save_copy = Button(self)
        self.save_copy['text'] = 'Save and Copy'
        self.save_copy['command'] = self.save_password
        self.save_copy.pack({'side':'left'})

        self.discard = Button(self)
        self.discard['text'] = 'Discard'
        self.discard['command'] = self.discard_password
        self.discard.pack({'side':'right'})

    def save_password(self):
        print('BEFORE CLOSING WINDOW - PASTE PASSWORD WHERE NEEDED!')
        self.master.clipboard_clear()
        self.master.clipboard_append(self.password)
        self.update()
        print('Saved password to clipboard and locked in vault.')

    def discard_password(self):
        print('Destorying password.')
        self.master.destroy()
