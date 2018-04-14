import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(credentials)


class Person:
    def __init__(self, person_name, num_msg, person_friends):
        self.n = person_name
        self.msg = num_msg
        self.assigned = 0
        self.ass_list = []
        self.friends_list = person_friends

    def __repr__(self):
        return self.n + ", " + str(self.msg)


class Friend:

    def __init__(self, friend_name):
        self.nm = friend_name
        self.num_friends = 1
        self.assigned = 0
        self.friends_list = []

    def __repr__(self):
        return self.nm + ", " + str(self.num_friends)

    def increment(self):
        self.num_friends += 1


def person_msg(person):
    return person.msg


def friend_friends(friend):
    return friend.num_friends


num_sheets = 1      # number of sheets within the workbook to pull data from
num_columns = 6     # number of people on each sheet
master_list = []    # list of people to be messaged
person_list = []    # list of people doing the messaging


i = 0

while i < num_sheets:

    sheet = client.open('Names')
    worksheet = sheet.get_worksheet(i)

    j = 2

    while j <= num_columns + 1:
        work_list = worksheet.col_values(j)     # creates list from facebook friends as pulled from spreadsheet
        work_list = list(filter(None, work_list))   # removes empty entries
        name = work_list[00]                    # sets persons name to first entry in column
        number_msg = int(work_list[1])          # sets the number to message equal to 2nd entry in column
        friends = work_list[2:]                 # takes remaining entries as friends list
        person_list.append(Person(name, number_msg, friends))   # creates person object out of above data
        friends = work_list[2:]
        k = 0
        while k < len(friends):                 # iterates through each persons friends list to build master_list
            counter = 0
            done = 0
            while counter < len(master_list) and done == 0:

                if friends[k] == master_list[counter].nm:   # filters for duplicates
                    done = 1
                    master_list[counter].increment()        # if duplicate, adds 1 to number of friends
                    master_list[counter].friends_list.append(name)  # if duplicate, adds person to friends list
                counter += 1
            if done == 0:
                master_list.append(Friend(friends[k]))      # if not duplicate, creates new friend object on master_list
                master_list[counter].friends_list.append(name)  # adds person to new friend object friends_list
            k += 1
        j += 1
    i += 1


master_list.sort(key=friend_friends)    # sorts list of people to be messaged in ascending order of the num of friends
person_list.sort(key=person_msg)        # sorts list of people messaging in ascending order of num to message

done = 0
i = 0               # master_list counter: person being assigned
j = 0               # person_list counter: person being assigned to
k = 0               # master_list[i].friends_list counter: increments through friends list of person being assigned

while i < len(master_list):
    done = 0
    j = 0
    while j < len(person_list) and done == 0:
        k = 0
        while k < len(master_list[i].friends_list) and done == 0 and person_list[j].assigned <= person_list[j].msg:
            if person_list[j].n == master_list[i].friends_list[k]:  # if match, assigns friend to person
                done = 1
                person_list[j].ass_list.append(master_list[i].nm)
                person_list[j].assigned += 1
                master_list[i].assigned = 1
            k += 1
        j += 1
    i += 1

sheet = client.open('Names')
worksheet = sheet.get_worksheet(num_sheets)

i = 0
j = 0

while i < len(person_list):         # outputs assignments to spreadsheet
    j = 1
    worksheet.update_cell(1, i + 1, person_list[i].n)
    while j < len(person_list[i].ass_list):
        worksheet.update_cell(j + 1, i + 1, person_list[i].ass_list[j])
        j += 1
        k += 1
    i += 1
