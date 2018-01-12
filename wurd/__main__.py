import argparse as arg
from . import __version__ as VERSION
from .wurd import NewWurdInstance, WurdInstance

    
def main():
    parser = arg.ArgumentParser()

    parser.add_argument('-i', '--init', help='Initializes a new Wurd Storage instance')
    parser.add_argument('-n', '--new', help='Creates a new password or updates an old one.')
    parser.add_argument('-g', '--get', help='Fetches a password.')
    parser.add_argument('-d', '--delete', help='Deletes a password.')
    parser.add_argument('--version', action='version', version=VERSION)

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
        p = wurd.generate_password()
        wurd.save_password(name, p)

    elif args['get']:
        name = args['get']
        wurd = WurdInstance()
        wurd.get_password(name)
        
    elif args['delete']:
        wurd = WurdInstance()
        wurd.delete_password(args['delete'])
        
        
if __name__ == '__main__':
    main()
