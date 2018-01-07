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


def append_password(name):
    root = tkinter.Tk()
    root.title('Your New Password')
    root.maxsize(256, 128)
    popup = NewPasswordPopup(name, master=root)
    popup.mainloop()
    
def main():
    parser = arg.ArgumentParser()

    parser.add_argument('-i', '--init', help='Initialize a new Wurd Storage instance')
    parser.add_argument('-n', '--new', help='Create a new password')
    parser.add_argument('-o', '--print', help='Print out of current passwords.')
    parser.add_argument('-f', '--fetch', help='Get password by name')
    parser.add_argument('-c', '--change', help='change password by name')
    parser.add_argument('-u', '---unlock', help='unlock using key')
    parser.add_argument('-d', '--delete', help='delete password by name')

    args = vars(parser.parse_args())

    if args['init']:
        name = args['init']
        create_new_wurd(name)
    
    elif args['new']:
        print('Your new password %s has been created!')
        print('It was saved under the name', args['new'])
        append_password(args['new'])

    elif args['fetch']:
        if args['unlock']:
            print('Unlocking your vault with', args['unlock'])
            print('Success!')
            with open('.wurd.dat', 'r') as f:
                for l in f.readlines():
                    l = l.split()
                    if l[0] == args['fetch']:
                        print('Found password.')
                        root.tkinter.Tk()
                        root.title('Your Password')
                        root.maxsize(256, 128)
                        popup = FetchPasswordPopup(password, master=root)
        else:
            print('You must provide a key in order to unlock your password.')
        
    else:
        print('No valid arguments given!')


if __name__ == '__main__':
    main()
