import gspread
import sys

from oauth2client.service_account import ServiceAccountCredentials

sheet_name = 'core.xlsx'
assignment_sheet_name = 'core assignments'

class Messenger:
    def __init__(self, messenger_name, friends_list):
        self.nm = messenger_name
        self.messenger_friends = friends_list
        self.ass_list = []
        self.num_friends = len(friends_list)


def messenger_num_friends(messenger):
    return messenger.num_friends


def build_messenger_list():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(credentials)
    messenger_list = []
    sheet = client.open(sheet_name)
    worksheet = sheet.get_worksheet(0)
    i = 1
    msngr_col = worksheet.col_values(i)
    while msngr_col[0] != '':
        msngr_name = msngr_col[0]
        del msngr_col[0]
        msngr_friends = list(filter(None, msngr_col))
        messenger_list.append(Messenger(msngr_name, msngr_friends))
        i += 1
        msngr_col = worksheet.col_values(i)
    messenger_list.sort(key=messenger_num_friends)
    print('Built messenger list from sheet: ' + sheet_name)
    return messenger_list


def assign_people(messenger_list):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(credentials)
    assignment_list = messenger_list
    assigned_file = open('assigned_people.txt','r')
    assigned_list = assigned_file.readlines()
    assigned_file.close()
    i = 0
    while i < len(assignment_list):
        j = 0
        while j < len(assignment_list[i].messenger_friends):
            current_person = assignment_list[i].messenger_friends[j]
            if current_person + '\n' not in assigned_list:
                assigned_list.append(current_person + '\n')
                assignment_list[i].ass_list.append(current_person)
            j += 1
        i += 1
    print_sheet = client.open(assignment_sheet_name)
    print_worksheet = print_sheet.get_worksheet(0)
    k = 1
    while k <= len(assignment_list):
        cell_values = [assignment_list[k-1].nm] + assignment_list[k-1].ass_list
        cell_list = print_worksheet.range(1, k, len(cell_values), k)
        for h, val in enumerate(cell_values):
            cell_list[h].value = val
        print_worksheet.update_cells(cell_list)
        k += 1
    assigned_file = open('assigned_people.txt','w')
    assigned_file.writelines(assigned_list)
    print('Assigned each person uniquely, outputted results to sheet: ' + assignment_sheet_name)
    return


def add_person(column_number):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(credentials)
    sheet = client.open(sheet_name)
    worksheet = sheet.get_worksheet(0)
    msngr_col = worksheet.col_values(column_number)
    name = msngr_col[0]
    del msngr_col[0]
    friends_list = list(filter(None, msngr_col))
    new_person = Messenger(name, friends_list)
    assigned_file = open('assigned_people.txt','r')
    assigned_list = assigned_file.readlines()
    assigned_file.close()
    i = 0
    while i < len(new_person.messenger_friends):
        current_person = new_person.messenger_friends[i]
        if current_person + '\n' not in assigned_list:
            assigned_list.append(current_person + '\n')
            new_person.ass_list.append(current_person)
        i += 1
    print_sheet = client.open(assignment_sheet_name)
    print_worksheet = print_sheet.get_worksheet(0)
    i = 3
    col_list = print_worksheet.col_values(i)
    while col_list[0] != '':
        i += 1
        col_list = print_worksheet.col_values(i)
    cell_values = [new_person.nm] + new_person.ass_list
    cell_list = print_worksheet.range(1, i, len(cell_values), i)
    for h, val in enumerate(cell_values):
        cell_list[h].value = val
    print_worksheet.update_cells(cell_list)
    assigned_file = open('assigned_people.txt','w')
    assigned_file.writelines(assigned_list)
    assigned_file.close()
    print('Produced assignment for '+new_person.nm+', output to '+assignment_sheet_name)
    return

def main():
    if len(sys.argv) == 1:
        assign_people(build_messenger_list())
    elif len(sys.argv) == 2:
        add_person(sys.argv[1])
    else:
        print('ya done fucked up')
        sys.exit()

if __name__ == '__main__':
    main()
