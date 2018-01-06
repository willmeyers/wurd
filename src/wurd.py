import argparse as arg
import utils
import datetime
from password import Password
import sqlite3
from cryptography.fernet import Fernet
import tkinter

import os


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
    create_new_db()
    
def create_new_key():
    print('Generating new key and saving to wurd.key')
    key = Fernet.generate_key()
    with open('wurd.key', 'w+') as f:
        f.write(key.decode())
    print('Done.')


def create_new_db():
    print('Inorder to keep your passwords safe, WURD requires a')
    print('MASTER PASSWORD to be used to encrypt the entire database.\n')

    print('Like the generated key, keep this password safe and memorized!')
    p = input('Enter master password > ')
    
    print('Creating new database...')
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('CREATE TABLE folders (id INTEGER PRIMARY KEY, name TEXT)')
    conn.commit()
    c.execute('CREATE TABLE passwords (id INTEGER PRIMARY KEY, folder INTEGER, name TEXT, passwd TEXT, FOREIGN KEY(folder) REFERENCES folders(id))')
    conn.commit()
    print('Done.')
    

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
        print('Started NEW PASSWORD prompt.')
        print('Follow the instructions below.')

        name = input('Give this password a name. (e.g. Work Email) > ')
        folder = input('Save this password in a folder? (y/n) > ')
        if folder.lower() == 'y':
            folder = input('Enter name of folder. (e.g. Social Media) > ')
        else: pass
        print(Password(name, folder).generate())

    else:
        print('No valid arguments given!')


if __name__ == '__main__':
    main()
