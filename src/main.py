import pyperclip
import argparse as arg
from password import Password
from db import NewWurdInstance, WurdInstance

    
def main():
    parser = arg.ArgumentParser()

    parser.add_argument('-i', '--init', help='Initialize a new Wurd Storage instance')
    parser.add_argument('-n', '--new', help='Creates a new password.')
    parser.add_argument('-f', '--fetch', help='Fetch a password.')
    parser.add_argument('-c', '--change', help='Change password to a custom password.')
    parser.add_argument('-d', '--delete', help='Deletes a password.')

    args = vars(parser.parse_args())

    if args['init']:
        print('\n+=============================================================+')
        print('|         Welcome to the WURD Password Setup Wizard!          |')
        print('|Follow the prompts below to setup your WURD password storage.|')
        print('+=============================================================+\n')

        input('Press [RETURN] to start')
        
        name = args['init']

        wurd = NewWurdInstance(name)

        print('Done.')
        
    elif args['new']:
        name = args['new']
        wurd = WurdInstance()

        passwd = Password(name).generate()
        
        print('Your new password for %s: %s' % (name, passwd))
        conf = input('Save this password? (yes/no) ')

        if conf.lower() == 'yes':
            pyperclip.copy(passwd)
            wurd.save_password(name, passwd)
            print('Password copied to clipboard.')
        else:
            print('Password discared.')

    elif args['fetch']:
        name = args['fetch']
        wurd = WurdInstance()
        passwd = wurd.fetch_password(name)
        print('Your password: ', passwd)
        pyperclip.copy(passwd)
        print('has been saved to your clipboard.')

    elif args['change']:
        pass

    elif args['delete']:
        pass
    
    else:
        print('No valid arguments given!')
        
        
if __name__ == '__main__':
    main()
