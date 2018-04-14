import os
import sys
import base64
from argon2 import PasswordHasher
from getpass import getpass
from Crypto.Cipher import AES

FILE_NAME = 'logins.csv'
iv = b"6'W:\xab\xe1Wt+\x94\xffg\xb6\xeb\xce\xa1"

class User:

    def __init__(self,name,username,password):
        self.name = name
        self.username = username
        self.password = password

    def __str__(self):
        return self.name+','+self.username+','+str(self.password)


def create_logins_file(login_list):


    write_file = open(FILE_NAME, 'a')
    i = 0
    while i < len(login_list):
        write_file.write(str(login_list[i]))
        write_file.write('\n')
        i += 1
    return


def get_user_obj(admin_password, iv):
    password_arg = str.encode(admin_password)
    crypt = AES.new(password_arg, AES.MODE_CFB, iv)
    name = input("Name: ")
    if name == 'done':
        return 'done'
    username = input('Username: ')
    password = getpass('Password: ')
    crypt_pass = crypt.encrypt(password)
    b64_pass = base64.b64encode(crypt_pass)
    str_pass = str(b64_pass, 'utf-8')
    password = os.urandom(8)
    usr_str = str(User(name, username, str_pass))
    del password
    del username
    return usr_str

def create_login_list(admin_password, iv):
    login_list = []
    while True:
        new_user = get_user_obj(admin_password, iv)
        if new_user == 'done':
            return login_list
        login_list.append(new_user)


def create_admin_account():
    private = getpass('New Password: ')
    private_salt = str(os.urandom(8))
    b64_iv = base64.b64encode(iv)
    str_vector = str(b64_iv, 'utf-8')
    hasher = PasswordHasher()
    private_hash = hasher.hash(private + private_salt)
    write_file = open('script_password_verification.txt','w')
    write_string = private_hash+';'+private_salt+';'+str_vector
    write_file.write(write_string)
    write_file.close()
    stats_file = open('stats.txt','w')
    stats_file.write('0')
    stats_file.close()
    ret_list = [private, iv]
    return ret_list


def verify_admin_account():
    password_try = getpass('Password: ')
    read_file = open('script_password_verification.txt','r')
    read_list = read_file.readlines()
    read_file.close()
    cred_list = read_list[0].split(';')
    hasher = PasswordHasher()
    try_hash = hasher.verify(cred_list[0], password_try+cred_list[1])
    if not try_hash:
        sys.exit('Password does not match')
    ret_list = [password_try, iv]
    return ret_list


def main():
    read_file = open(FILE_NAME, 'r')
    lines = read_file.readlines()
    lines = list(filter(None, lines))
    if len(lines) < 2:
        creds = create_admin_account()
    else:
        creds = verify_admin_account()
    login_list = create_login_list(creds[0], creds[1])
    create_logins_file(login_list)

if __name__ == "__main__":
    main()
