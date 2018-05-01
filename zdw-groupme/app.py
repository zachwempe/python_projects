import os
import json
import requests
import gspread

from urllib.parse import urlencode
from urllib.request import Request, urlopen
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask,

# This is a GroupMe bot used to keep campaign members aware of their schedule of shifts
# for running campaign tables on campus. Users could send 'my schedule' in a GroupMe group
# and receive a message back detailing their schedule as far out as it had been scheduled.
# Given that the bot was updated every night and the format of each schedule could differ greatly from day to day,
# I opted to simply copy-paste and find-and-replace so that the bot could be updated as quickly as possible
# despite this making the code uglier and less in line with standard coding practices.

app = Flask(__name__)

def send_message(text):
    print('entered message method')
    print(os.getenv('GROUPME_BOT_ID'))
    url = "https://api.groupme.com/v3/bots/post"
    msg = {"bot_id": (os.getenv('GROUPME_BOT_ID')), "text": text}
    r = requests.post(url, data=msg)
    print('made it past post request')

    return


@app.route('/', methods=['POST'])
def webhook():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(credentials)
    print('entered webhook')
    data = request.get_json()
    sheet = client.open('Tabling Schedule Runoff')
    tues_sheet = sheet.get_worksheet(1)
    tues_west_mall_list = tues_sheet.col_values(2)
    tues_speedway_list = tues_sheet.col_values(4)
    tues_pcl_list = tues_sheet.col_values(6)
    tues_wm_830_9 = [x.lower() for x in tues_west_mall_list[3:7]]
    tues_wm_9_10 = [x.lower() for x in tues_west_mall_list[7:13]]
    tues_wm_10_11 = [x.lower() for x in tues_west_mall_list[13:19]]
    tues_wm_11_12 = [x.lower() for x in tues_west_mall_list[19:25]]
    tues_wm_12_1 = [x.lower() for x in tues_west_mall_list[25:31]]
    tues_wm_1_2 = [x.lower() for x in tues_west_mall_list[31:37]]
    tues_wm_2_3 = [x.lower() for x in tues_west_mall_list[37:43]]
    tues_wm_3_330 = [x.lower() for x in tues_west_mall_list[43:46]]
    tues_sw_830_9 = [x.lower() for x in tues_speedway_list[3:7]]
    tues_sw_9_10 = [x.lower() for x in tues_speedway_list[7:13]]
    tues_sw_10_11 = [x.lower() for x in tues_speedway_list[13:19]]
    tues_sw_11_12 = [x.lower() for x in tues_speedway_list[19:25]]
    tues_sw_12_1 = [x.lower() for x in tues_speedway_list[25:31]]
    tues_sw_1_2 = [x.lower() for x in tues_speedway_list[31:37]]
    tues_sw_2_3 = [x.lower() for x in tues_speedway_list[37:43]]
    tues_sw_3_330 = [x.lower() for x in tues_speedway_list[43:46]]
    tues_eng_830_9 = [x.lower() for x in tues_pcl_list[3:7]]
    tues_eng_9_10 = [x.lower() for x in tues_pcl_list[7:13]]
    tues_eng_10_11 = [x.lower() for x in tues_pcl_list[13:19]]
    tues_eng_11_12 = [x.lower() for x in tues_pcl_list[19:25]]
    tues_eng_12_1 = [x.lower() for x in tues_pcl_list[25:31]]
    tues_eng_1_2 = [x.lower() for x in tues_pcl_list[31:37]]
    tues_eng_2_3 = [x.lower() for x in tues_pcl_list[37:43]]
    tues_eng_3_330 = [x.lower() for x in tues_pcl_list[43:46]]
    print(tues_sw_9_10)

    if data['name'] != 'Tabling Schedule':
        if (data['text'][:11]).lower() == 'my schedule':
            shift_list = []
            msg = data['name']+', your shifts for this upcoming week are as follows:\n'
            data['name'] = (data['name']).lower()
            if data['name'] in tues_wm_830_9:
                shift_list.append('Tuesday 8:30-9:00 West Mall Setup')
            if data['name'] in tues_wm_9_10:
                shift_list.append('Tuesday 9:00-10:00 West Mall')
            if data['name'] in tues_wm_10_11:
                shift_list.append('Tuesday 10:00-11:00 West Mall')
            if data['name'] in tues_wm_11_12:
                shift_list.append('Tuesday 11:00-12:00 West Mall')
            if data['name'] in tues_wm_12_1:
                shift_list.append('Tuesday 12:00-1:00 West Mall')
            if data['name'] in tues_wm_1_2:
                shift_list.append('Tuesday 1:00-2:00 West Mall')
            if data['name'] in tues_wm_2_3:
                shift_list.append('Tuesday 2:00-3:00 West Mall')
            if data['name'] in tues_wm_3_330:
                shift_list.append('Tuesday 3:00-3:30 West Mall Breakdown')
            if data['name'] in tues_sw_830_9:
                shift_list.append('Tuesday 8:30-9:00 Speedway Setup')
            if data['name'] in tues_sw_9_10:
                shift_list.append('Tuesday 9:00-10:00 Speedway')
            if data['name'] in tues_sw_10_11:
                shift_list.append('Tuesday 10:00-11:00 Speedway')
            if data['name'] in tues_sw_11_12:
                shift_list.append('Tuesday 11:00-12:00 Speedway')
            if data['name'] in tues_sw_12_1:
                shift_list.append('Tuesday 12:00-1:00 Speedway')
            if data['name'] in tues_sw_1_2:
                shift_list.append('Tuesday 1:00-2:00 Speedway')
            if data['name'] in tues_sw_2_3:
                shift_list.append('Tuesday 2:00-3:00 Speedway')
            if data['name'] in tues_sw_3_330:
                shift_list.append('Tuesday 3:00-3:30 Speedway Breakdown')
            if data['name'] in tues_eng_830_9:
                shift_list.append('Tuesday 8:30-9:00 PCL Setup')
            if data['name'] in tues_eng_9_10:
                shift_list.append('Tuesday 9:00-10:00 PCL')
            if data['name'] in tues_eng_10_11:
                shift_list.append('Tuesday 10:00-11:00 PCL')
            if data['name'] in tues_eng_11_12:
                shift_list.append('Tuesday 11:00-12:00 PCL')
            if data['name'] in tues_eng_12_1:
                shift_list.append('Tuesday 12:00-1:00 PCL')
            if data['name'] in tues_eng_1_2:
                shift_list.append('Tuesday 1:00-2:00 PCL')
            if data['name'] in tues_eng_2_3:
                shift_list.append('Tuesday 2:00-3:00 PCL')
            if data['name'] in tues_eng_3_330:
                shift_list.append('Tuesday 3:00-3:30 PCL Breakdown')

            i = 0

            print(shift_list)
            print(len(shift_list))
            while i < len(shift_list):
                print(shift_list[i])
                msg += shift_list[i]
                msg += '\n'
                i+= 1
            print(msg)
            send_message(msg)


        if (data['text']).lower() == 'tuesday 8:30-9:00 west mall':
            msg = 'The following people are scheduled:\n'
            i = 0
            while i < len(tues_wm_830_9):
                msg += tues_wm_830_9[i]
                if tues_wm_830_9[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 9:00-10:00 west mall':
            msg = 'The following people are scheduled:\n'
            i = 0
            while i < len(tues_wm_9_10):
                msg += tues_wm_9_10[i]
                if tues_wm_9_10[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 10:00-11:00 west mall':
            msg = 'The following people are scheduled\n'
            i = 0
            while i < len(tues_wm_10_11):
                msg += tues_wm_10_11[i]
                if tues_wm_10_11[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 11:00-12:00 west mall':
            msg = 'The following people are scheduled:\n'
            i = 0
            while i < len(tues_wm_11_12):
                msg += tues_wm_11_12[i]
                if tues_wm_11_12[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 12:00-1:00 west mall':
            msg = 'The following people are scheduled:\n'
            i = 0
            while i < len(tues_wm_12_1):
                msg += tues_wm_12_1[i]
                if tues_wm_12_1[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 1:00-2:00 west mall':
            msg = 'The following people are scheduled:\n'
            i = 0
            while i < len(tues_wm_1_2):
                msg += tues_wm_1_2[i]
                if tues_wm_1_2[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 2:00-3:00 west mall':
            msg = 'The following people are scheduled:\n'
            i = 0
            while i < len(tues_wm_2_3):
                msg += tues_wm_2_3[i]
                if tues_wm_2_3[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 8:30-9:00 speedway':
            msg = 'The following people are scheduled:\n'
            i = 0
            while i < len(tues_sw_830_9):
                msg += tues_sw_830_9[i]
                if tues_sw_830_9[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 9:00-10:00 speedway':
            msg = 'The following people are scheduled:\n'
            i = 0
            while i < len(tues_sw_9_10):
                msg += tues_sw_9_10[i]
                if tues_sw_9_10[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 10:00-11:00 speedway':
            msg = 'The following people are scheduled\n'
            i = 0
            while i < len(tues_sw_10_11):
                msg += tues_sw_10_11[i]
                if tues_sw_10_11[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 11:00-12:00 speedway':
            msg = 'The following people are scheduled:\n'
            i = 0
            while i < len(tues_sw_11_12):
                msg += tues_sw_11_12[i]
                if tues_sw_11_12[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 12:00-1:00 speedway':
            msg = 'The following people are scheduled:\n'
            i = 0
            while i < len(tues_sw_12_1):
                msg += tues_sw_12_1[i]
                if tues_sw_12_1[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 1:00-2:00 speedway':
            msg = 'The following people are scheduled:\n'
            i = 0
            while i < len(tues_sw_1_2):
                msg += tues_sw_1_2[i]
                if tues_sw_1_2[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 2:00-3:00 speedway':
            msg = 'The following people are scheduled:\n'
            i = 0
            while i < len(tues_sw_2_3):
                msg += tues_sw_2_3[i]
                if tues_sw_2_3[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 8:30-9:00 pcl':
            msg = 'The following people are scheduled:\n'
            i = 0
            while i < len(tues_eng_830_9):
                msg += tues_eng_830_9[i]
                if tues_eng_830_9[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 9:00-10:00 pcl':
            msg = 'The following people are scheduled:\n'
            i = 0
            while i < len(tues_eng_9_10):
                msg += tues_eng_9_10[i]
                if tues_eng_9_10[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 10:00-11:00 pcl':
            msg = 'The following people are scheduled\n'
            i = 0
            while i < len(tues_wm_10_11):
                msg += tues_wm_10_11[i]
                if tues_wm_10_11[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 11:00-12:00 pcl':
            msg = 'The following people are scheduled:\n'
            i = 0
            while i < len(tues_eng_11_12):
                msg += tues_eng_11_12[i]
                if tues_eng_11_12[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 12:00-1:00 pcl':
            msg = 'The following people are scheduled:\n'
            i = 0
            while i < len(tues_eng_12_1):
                msg += tues_eng_12_1[i]
                if tues_eng_12_1[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 1:00-2:00 pcl':
            msg = 'The following people are scheduled:\n'
            i = 0
            while i < len(tues_eng_1_2):
                msg += tues_eng_1_2[i]
                if tues_eng_1_2[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)
        if (data['text']).lower() == 'tuesday 2:00-3:00 pcl':
            msg = 'The following people are scheduled:\n'
            i = 0
            while i < len(tues_eng_2_3):
                msg += tues_eng_2_3[i]
                if tues_eng_2_3[i] != '':
                    msg += '\n'
                i += 1
            send_message(msg)


    return "ok", 200
