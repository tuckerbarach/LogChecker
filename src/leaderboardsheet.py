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
sheet = client.open('LogChecker Leaderboards').sheet1


def get_name(index):
    refresh_token()
    return sheet.cell(index, 1).value

def get_score(index):
    refresh_token()
    try:
        return sheet.cell(index, 2).value
    except:
        return

def update_member_score(user):
    refresh_token()
    current_score = sheet.cell(sheet.find(user).row, 2).value
    sheet.update_cell(sheet.find(user).row, 2, int(current_score) + 1)

def get_player_score(user):
    refresh_token()
    return sheet.cell(sheet.find(user).row, 2).value

def refresh_token():
    if creds.access_token_expired:
        client.login()  # refreshes the token