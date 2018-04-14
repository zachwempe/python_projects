
# -*- coding: utf-8 -*-

import fbchat
import gspread
import random
import time

from oauth2client.service_account import ServiceAccountCredentials
from getpass import getpass

# This version of the campaign facebook bot was the initial quick-and-dirty (~5-day timeline) attempt
# at automating our campaign facebook messaging. Various issues were run into over the course of
# usage but we were able to send around 4000 automated messages from about 20 facebook accounts belonging to campaign
# members.


scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
gclient = gspread.authorize(credentials)
sheet = gclient.open('Assignments')
actual_sheet = sheet.get_worksheet(0)
username = str(raw_input('Username:'))
client = fbchat.Client(username, getpass())
names = actual_sheet.col_values(10)
i = 0
# new_sheet = gclient.open('DO NOT MESSAGE')
# new_worksheet = new_sheet.get_worksheet(0)
# stats_sheet = gclient.open("Keepin' Track of Stuff")
# stats_worksheet = stats_sheet.get_worksheet(0)
# num_sent_cell = stats_worksheet.cell(1, 2)
# num_sent = int(num_sent_cell.value)
# naughty_list = new_worksheet.col_values(1)
# naughty_list = list(filter(None, naughty_list))
names = list(filter(None, names))
names = names[2:]
while i < len(names):
    friends = client.searchForUsers(names[i])
    if len(friends) > 0:
        friend = friends[0]
        print(names[i])
        if True:
            both_name = names[i].split()
            firstname = both_name[0]
            msg3 = "Hi "+firstname+"! I'm helping Colton Becker and Mehraz Rahman run for Student Body President/VP, and I would love it if you could vote for them! Visit this website to vote: https://goo.gl/455D7b "
            msg4 = "Do you think we should have more reflection spaces at UT? Vote for Colton and Mehraz as student body president and VP here: https://goo.gl/z6c1Z2"
            msg7 = "Interpersonal violence is a huge issue at UT that should actively be addressed. Colton and Mehraz are the only campaign that are including this issue in their platform. A vote for Colton and Mehraz for president and VP is a vote for interpersonal violence prevention. Vote here: https://goo.gl/iB86fM"
            msg_list = [msg3, msg4, msg7]
            #msg = "Hey "+firstname+"! I'm sure you've heard, but voting for Executive Alliances are opening up again! My good friend Mehraz and I are running for President and VP, and we've worked hard on this campaign to create a vision we believe can improve the life of every Longhorn. The both of us would appreciate your support! Vote today until 5pm tomorrow at https://goo.gl/9yhnXb and tell your friends! Let's Get Started!"
            #msg = ("hey "+firstname+"! voting for student government is opening up AGAIN today at 8 am!! Colton Becker and I are running for Student Body President and Vice President, and your support and vote would mean so so much :~) you can vote until 5pm tomorrow at https://goo.gl/pv3H7v ! we've spoken to students from all corners of campus and crafted a platform that I really believe in, including issues I'm passionate about like mental health policies, interpersonal violence prevention,"       +" and adding more reflection spaces to campus! let's! get! started :~) ")
            sent = client.send(fbchat.Message(msg), friend.uid)
        #     if sent:
        #         num_sent += 1
        # print(num_sent)

    i += 1
# stats_worksheet.update_cell(1, 2, num_sent)
