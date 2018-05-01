import fbchat
import random
import time
import os
import base64

from Crypto.Cipher import AES
from oauth2client.service_account import ServiceAccountCredentials
from getpass import getpass
from argon2 import PasswordHasher

iv = b"6'W:\xab\xe1Wt+\x94\xffg\xb6\xeb\xce\xa1"
people_per_hour_per_account = 50

"""
This version of the campaign facebook bot is a quick-and-dirty (~4-day timeline)
attempt at getting around facebook's blocking strategies in an effort to send more messages.
Other issues were run into preventing us from sending as many messages before, but due to the
accelerated timeline we were unable to predict/diagnose/fix these issues ahead of time.
"""
class Person:

    def __init__(self, name, client):
        self.name = name
        self.client = client

def main():
    password = getpass()
    password_arg = str.encode(password)
    logins_file = open('logins.csv','r')
    logins_list = logins_file.readlines()
    logins_file.close()
    num_users = len(logins_list)
    seconds_per_message = (3600/num_users)/people_per_hour_per_account + 2
    i = 0
    k = 0
    num_sent = 0
    while k < len(logins_list):
        person_list = []
        num_logins = len(logins_list)
        while len(person_list) < num_logins:
            crypt = AES.new(password_arg, AES.MODE_CFB, iv)
            current_user = logins_list[i].split(',')
            name = current_user[0]
            name = current_user[0]
            name = name.replace(' ','')
            username = current_user[1]
            password = current_user[2]
            b64_pass = bytes(password, 'utf-8')
            crypt_pass = base64.b64decode(b64_pass)
            str_pass = crypt.decrypt(crypt_pass)
            str_pass = str_pass.decode('utf-8')
            try:
                new_client = fbchat.Client(username, str_pass)
                person_list.append(Person(name, new_client))
            except fbchat.models.FBchatUserError:
                num_logins -= 1
            i += 1
        i = 0
        go_round_counter = 0
        while go_round_counter < 5:
            while i < len(person_list):
                stats_file = open('stats.txt', 'r')
                stats_list = stats_file.readlines()
                stats_file.close()
                num_sent = int(stats_list[0])
                name = person_list[i].name
                file_name = name + '.txt'
                user_file = open('assignments/' + file_name, 'r')
                user_list = user_file.readlines()
                user_file.close()
                j = 0
                message_file = open('messages/' + file_name, 'r')
                message_list = message_file.readlines()
                message_file.close()
                link_file = open('links.txt','r')
                link_list = link_file.readlines()
                link_file.close()
                if len(user_list) == 0:
                    k += 1
                while j < len(user_list) and j < people_per_hour_per_account:
                    name = user_list[j][:-1]
                    message = random.choice(message_list)
                    friends = person_list[i].client.searchForUsers(name)
                    first_name = name.split()[0]
                    link = random.choice(link_list)[:-1]
                    msg = message.format(first_name, link)
                    if len(friends) > 0:
                        sent = True
                        friend = friends[0]
                        try:
                            message_id = person_list[i].client.send(fbchat.Message(msg), friend.uid)
                            sent = True
                        except fbchat.models.FBchatFacebookError:
                            sent = False
                        if sent:
                            num_sent += 1
                            print(name)
                            print(num_sent)
                            del user_list[j]
                    else:
                        del user_list[j]
                    time.sleep(4)
                    j += 1
                user_file = open('assignments/' + file_name, 'w')
                user_file.writelines(user_list)
                user_file.close()
                stats_file = open('stats.txt', 'w')
                stats_file.write(str(num_sent))
                stats_file.close()
                i += 1
            go_round_counter += 1
        i = 0
    print('Sent '+str(num_sent)+' messages, zach truly is the spam god')
    return

if __name__ == '__main__':
    main()
