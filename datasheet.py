import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint as pp

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Storing Log Files').sheet1


def store_data(realm, data):
    if realm == "Onyx":
        sheet.update_cell(2, 2, data)

# row = ["I'm", "updating", "a", "spreadsheet", "from", "Python!"]
# index = 3
# sheet.insert_row(row, index)
# sheet.delete_row(3)

# result = sheet.update_cell(2, 2, "check out this amazing log file\n\n\nhi") # Update cell
# result = sheet.cell(2, 2).value #Today's Onyx file
# result = sheet.row_values(1) # Prints top row
# result = sheet.col_values(1) # Prints first column
# result = sheet.get_all_records()
# pp.pprint(result)
# print(sheet.row_count)
