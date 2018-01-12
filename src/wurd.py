import os
import sys
import sqlite3
import yaml
from getpass import getpass
from datetime import datetime

from password import Password

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


SCHEMA = ('CREATE TABLE IF NOT EXISTS passwords ('
          'id INTEGER PRIMARY KEY,'
          'name TEXT NOT NULL,'
          'created_on TEXT NOT NULL,'
          'updated_on TEXT NOT NULL,'
          'password TEXT NOT NULL'
          ');'
)


INSERT_PASSWD = ('INSERT INTO passwords ('
                 'name,'
                 'created_on,'
                 'updated_on,'
                 'password'
                 ')'
                 'VALUES ('
                 '{0}, {1}, {2}, {3}'
                 ');'
)


class NewWurdInstance:
    def __init__(self, name):
        self.name = name + '.db'
        self.wurd_path = self.create_wurd_directory()
        
        self.create_database()
        self.create_keys()
        self.create_config()
        
    def create_wurd_directory(self):
        ho = os.path.expanduser('~')
        
        try:
            os.mkdir(os.path.join(ho, '.wurd'))

        except OSError as e:
            print('Unable to create wurd directory.')
            print(e)

        p = os.path.join(ho, '.wurd')
        print('Created wurd directory:', p)
        return p
        
    def create_database(self):
        db_path = os.path.join(self.wurd_path, self.name)
        
        try:
            conn = sqlite3.connect(db_path)
            print('Successfully connected to ', self.name)
            print(sqlite3.version)
            print('Created ', datetime.now())
            self.create_tables(conn)
            
        except sqlite3.Error as e:
            print(e)

        finally:
            conn.close()

    def create_tables(self, conn):
        try:
            c = conn.cursor()
            c.execute(SCHEMA)
        except sqlite3.Error as e:
            print(e)

    def create_keys(self):
        print('Generating new RSA private and public keys...') 
        keys = rsa.generate_private_key(
            public_exponent = 65537,
            key_size = 2048,
            backend = default_backend()
        )

        print('Wurd encrypts your private key to ensure security.')
        print('We require a secure master password to do so.')

        master = getpass('You secure passphrase:')
        if getpass('Confirm your passphase:') != master:
            print('Passphrases did not match!')
            print('Exiting wizard!')
            sys.exit(1)
        
        pri_pem = keys.private_bytes(
            encoding = serialization.Encoding.PEM,
            format = serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm = serialization.BestAvailableEncryption(master.encode())
        )
        
        pub_pem = keys.public_key().public_bytes(
            encoding = serialization.Encoding.PEM,
            format = serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        with open(os.path.join(self.wurd_path, 'wurd_private_key.pem'), 'wb+') as f:
            print('Writing private key to', self.wurd_path)
            for line in pri_pem.splitlines():
                l = line + '\n'.encode()
                f.write(l)

        with open(os.path.join(self.wurd_path, 'wurd_public_key.pem'), 'wb+') as f:
            print('Writing public key to', self.wurd_path)
            for line in pub_pem.splitlines():
                l = line + '\n'.encode()
                f.write(l)

    def create_config(self):
        conf = {
            'path': self.wurd_path,
            'database': {
                'name': self.name,
                'version': sqlite3.version,
                'created on': datetime.now()
            },
            'keys': {
                'private key': os.path.join(self.wurd_path, 'wurd_private_key.pem'),
                'public key': os.path.join(self.wurd_path, 'wurd_public_key.pem'),
            },
            'log': {
                'last accessed': datetime.now(),
                'last updated': None,
                'last command': None
            }
        }
        
        with open(os.path.join(self.wurd_path, 'config.yml'), 'w+') as f:
            print('Writing config file to', self.wurd_path)
            yaml.dump(conf, f, default_flow_style=False)

            
class WurdInstance:
    def __init__(self):
        self.config = None
        self.wurd_path = os.path.join(os.path.expanduser('~'), '.wurd')

        with open(os.path.join(self.wurd_path, 'config.yml'), 'r') as f:
            self.config = yaml.load(f)
        
    def connect(self):
        db_name = self.config['database']['name']
        
        try:
            conn = sqlite3.connect(os.path.join(self.wurd_path, db_name))
            print('Successfully connected to ', db_name)
            
        except sqlite3.Error as e:
            print(e)

        return conn
    
    def load_private_key(self):
        with open(os.path.join(self.wurd_path, 'wurd_private_key.pem'), 'rb') as k:
            print('Reading private key from', self.wurd_path)
            pri_key = serialization.load_pem_private_key(
                k.read(),
                password = getpass('Enter your master passphrase:').encode(),
                backend = default_backend()
            )

        return pri_key

    def load_public_key(self):
        with open(os.path.join(self.wurd_path, 'wurd_public_key.pem'), 'rb') as k:
            print('Reading public key from', self.wurd_path)
            pub_key = serialization.load_pem_public_key(
                k.read(),
                backend = default_backend()
            )

        return pub_key
    
    def save_password(self, name, password):
        conn = self.connect()

        pub_key = self.load_public_key()

        print('Encrypting password using public key.')
        ciph = pub_key.encrypt(
            password.encode(),
            padding.OAEP(
                mgf = padding.MGF1(algorithm=hashes.SHA1()),
                algorithm = hashes.SHA1(),
                label = None
            )
        )

        cur = conn.cursor()
        insert_sql = ('INSERT INTO passwords ('
                      'name,'
                      'created_on,'
                      'updated_on,'
                      'password'
                      ')'
                      'VALUES (?,?,?,?);'
        )

        now = datetime.now().strftime('%d-%m-%Y %H:%M:%S%p')
        cur.execute(insert_sql, (name, now, now, ciph))
        
        print('Inserted password for %s into wurd database on %s.' % (name, now))

        conn.commit()
        conn.close()

    def fetch_password(self, name):
        conn = self.connect()
        cur = conn.cursor()

        pri_key = self.load_private_key()

        print('Fetching password...')
        p = cur.execute('SELECT password FROM passwords WHERE name = \'%s\'' % name)
        p = p.fetchone()[0]

        plain = pri_key.decrypt(
            p,
            padding.OAEP(
                mgf = padding.MGF1(algorithm=hashes.SHA1()),
                algorithm = hashes.SHA1(),
                label = None
            )
        )

        print('Done.')
        
        conn.close()

        return plain.decode()
        
    def delete_password(self, name):
        pass
