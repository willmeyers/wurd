import argparse as arg
import datetime
from password import Password
import sqlite3
from cryptography.fernet import Fernet
import tkinter
import os
from popup import *


def create_new_wurd(name):
    print('\n+=============================================================+')
    print('|         Welcome to the WURD Password Setup Wizard!          |')
    print('|Follow the prompts below to setup your WURD password storage.|')
    print('+=============================================================+\n')

    input('Press [RETURN] to start')
    
    print('The WURD file will be saved in you HOME directory as .wurd.db\n')
    print('WURD uses symmetric encryption to store and retrieve passwords.')
    print('This requires you to create an Fernet key.\n')
    print('The generated key will be saved in the HOME directory.')
    print('MAKE SURE TO KEEP THIS KEY SAFE! DO NOT LOSE THIS KEY!')
    print('YOU NEED IT TO ENCRYPT AND DECRYPT YOUR PASSWORDS!\n')

    input('I understand. [RETURN]')

    create_new_key()
    create_new_bin()

    print('Finished.')

    
def create_new_key():
    print('Generating new key and saving to wurd.key')
    key = Fernet.generate_key()
    with open('wurd.key', 'w+') as f:
        f.write(key.decode())
    print('Done.')


def create_new_bin():
    print('Creating new WURD file in HOME directory...')
    f = open('.wurd.dat', 'a+')
    f.close()
    print('Done.')


def append_password(name, password):
    root = tkinter.Tk()
    root.title('Your New Password')
    root.maxsize(256, 128)
    popup = PasswordPopup()
    popup.mainloop()
    root.destroy()
    
def main():
    parser = arg.ArgumentParser()

    parser.add_argument('-i', '--init', help='Initialize a new Wurd Storage instance')
    parser.add_argument('-n', '--new', help='Create a new password')
    parser.add_argument('-o', '--print', help='Print out of current passwords.')
    parser.add_argument('-p', '--password', help='Get password by name')
    parser.add_argument('-u', '--update', help='change password by name')
    parser.add_argument('-d', '--delete', help='delete password by name')

    args = vars(parser.parse_args())

    if args['init']:
        name = args['init']
        create_new_wurd(name)
    
    elif args['new']:
        print('Follow the instructions below.')
        print('A secure password will be shown shortly...')
        p = Password(args['new'], '').generate()
        append_password(args['new'], p)

    else:
        print('No valid arguments given!')


if __name__ == '__main__':
    main()
