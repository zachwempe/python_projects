import gspread
from oauth2client.service_account import ServiceAccountCredentials
from multiprocessing import Pool, Manager

class Messenger:
    def __init__(self, messenger_name, friends_list, num_msg):
        self.nm = messenger_name
        self.messenger_friends = friends_list
        self.ass_list = []
        self.num_friends = len(friends_list)
        self.num_msg = num_msg


def messenger_num(messenger):
    return messenger.num_msg


num_sheets = 1

def build_messenger_list():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(credentials)
    i = 0
    messenger_list = []
    while i < num_sheets:
        sheet = client.open('All Friends Lists')
        worksheet = sheet.get_worksheet(i)
        j = 29
        msngr_col = worksheet.col_values(j)
        while j <= 29:
            msngr_col = list(filter(None, msngr_col))
            name = msngr_col[0]
            print(name)
            num_msg = msngr_col[1]
            msngr_friends = msngr_col[2:]
            if len(msngr_friends) > 0:
                messenger_list.append(Messenger(name, msngr_friends, num_msg))
                print('added'+str(j))
            j += 1
            msngr_col = worksheet.col_values(j)
        i += 1
    messenger_list.sort(key=messenger_num)
    print('built list')
    return messenger_list


def assign_people(messenger_list):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(credentials)
    sheet = client.open("Keepin' Track of Stuff")
    worksheet = sheet.get_worksheet(0)
    assignment_list = messenger_list
    assigned_list = worksheet.col_values(1)
    assigned_list = list(filter(None, assigned_list))
    i = 0
    while i < len(assignment_list):
        j = 0
        while j < len(assignment_list[i].messenger_friends):
            current_person = assignment_list[i].messenger_friends[j]
            if current_person not in assigned_list:
                assigned_list.append(current_person)
                assignment_list[i].ass_list.append(current_person)
            j += 1
        i += 1
    print(assignment_list[0].ass_list)
    print_sheet = client.open('Assignments')
    print_worksheet = print_sheet.get_worksheet(0)
    k = 1
    i = 29
    while k <= len(assignment_list):
        cell_values = [assignment_list[k-1].nm] + assignment_list[k-1].ass_list
        print(i)
        cell_list = print_worksheet.range(1, i, len(cell_values), i)
        for h, val in enumerate(cell_values):
            cell_list[h].value = val
        print_worksheet.update_cells(cell_list)
        i += 1
        k += 1
    return


def add_person(sheet_number, column_number):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(credentials)
    sheet = client.open('All Friends Lists')
    worksheet = sheet.get_worksheet(sheet_number)
    msngr_col = worksheet.col_values(column_number)
    msngr_col = list(filter(None, msngr_col))
    name = msngr_col[0]
    friends_list = msngr_col[1:]
    new_person = Messenger(name, friends_list)
    ass_sheet = client.open("Keepin' Track of Stuff")
    ass_worksheet = ass_sheet.get_worksheet(0)
    assigned_list = ass_worksheet.col_values(1)
    assigned_list = list(filter(None, assigned_list))
    i = 0
    print('got assigned list')
    while i < len(new_person.messenger_friends):
        current_person = new_person.messenger_friends[i]
        if current_person not in assigned_list:
            assigned_list.append(current_person)
            new_person.ass_list.append(current_person)
        i += 1
    i = 1
    j = 0
    print('assigned people')
    print_sheet = client.open('test')
    print_worksheet = print_sheet.get_worksheet(0)
    print_worksheet.update_cell(1, 1, 'Holden Hopkins')
    i = 2
    while i < len(new_person.ass_list) + 2:
        print_worksheet.update_cell(i, 1, new_person.ass_list[i-2])
        i += 1
    return


messenger_list = build_messenger_list()
assign_people(messenger_list)
