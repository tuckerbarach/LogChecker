import gspread
from oauth2client.service_account import ServiceAccountCredentials
import schedule
import urllib
import os
import zipfile
import time
import datetime

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

if creds.access_token_expired:
    client.login()  # refreshes the token

client = gspread.authorize(creds)
sheet = client.open('Storing Log Files').sheet1

realm_cell = {
    "onyx": 2,
    "amber": 3,
    "ruby": 4,
    "origins": 5,
    "genesis": 6,
    "chaos": 7,
    "robbery": 8,
    "azkaban": 9,
    "rust": 10
}


def create_new_row():
    date = datetime.datetime.today()
    date = [date.strftime('%m-%d-%Y')]  # Year, month, day format
    sheet.insert_row(date, 2)  # Makes new row the very top


def get_data(realm, date):
    cell_index = realm_cell[realm]
    link = sheet.cell(sheet.find(date).row, cell_index).value
    contents = regular_contents(link)
    return contents


def store_data(realm, link):
    cell_index = realm_cell[realm]

    # result = sheet.cell(2, 2).value #Today's Onyx file
    if sheet.cell(2, cell_index).value == '':
        sheet.update_cell(2, cell_index, link)

    else:
        date_of_stored_log = first_start_time(link)

        if date_of_stored_log == first_start_time(sheet.cell(2, cell_index).value):
            replace_link(link, cell_index)
        elif date_of_stored_log != first_start_time(sheet.cell(2, cell_index).value):
            update_link(link, cell_index)


def update_link(new_link, index):
    current_link = sheet.cell(2, index).value
    sheet.update_cell(2, index, current_link + "," + new_link)


def replace_link(link, index):
    links = sheet.cell(2, index).value.split(",")
    links[-1] = link
    new_links = ""
    for i in range(len(links)):
        new_links += links[i] + ","
    new_links = new_links[0:-1]
    sheet.update_cell(2, index, new_links)


def zip_contents(link):
    try:
        urllib.request.urlretrieve(link, "LinkedFile123.zip")
    except:
        print("Something went wrong!")

    with zipfile.ZipFile("LinkedFile123" + ".zip", 'r') as zip_ref:
        zip_ref.extractall("LinkedFile123")
    os.remove("LinkedFile123.zip")
    myfile = open(os.getcwd() + "/LinkedFile123/" + os.listdir(os.getcwd() + "/LinkedFile123")[0], "r",
                  encoding="utf8")
    contents = myfile.read()
    myfile.close()
    os.remove(os.getcwd() + "/LinkedFile123/" + os.listdir(os.getcwd() + "/LinkedFile123")[0])
    return contents


def regular_contents(link):
    return_contents = ""
    links = link.split(",")
    for l in links:
        return_contents += zip_contents(l)
    return return_contents


def start_time_contents(link):
    return_contents = ""
    links = link.split(",")
    for l in links:
        return_contents = zip_contents(l) + return_contents
    return return_contents


def first_start_time(link):
    contents = start_time_contents(link)
    date = contents[contents.find("["):contents.find("]") + 1]
    return date
