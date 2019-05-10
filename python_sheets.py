from pprint import pprint
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import sys

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

# Opening the sheet
sheet = client.open(
    "Indorse Python Validator | Special Assignment (Responses)").sheet1


last_read_row = int(sheet.cell(2, 14).value)
total_rows = int(sheet.cell(1, 14).value)

# creating a list of the github user profiles which have to be checked and a list of the rows that they belong too
github_user_list = []
user_cell_range = []


def getting_github_user_list():
    global last_read_row
    global user_cell_range
    if last_read_row < 2:
        last_read_row = 2
        user_cell_range = list(range(last_read_row, total_rows + 2))
        for i in range(last_read_row, total_rows+2):
            github_user_list.append(sheet.cell(i, 5).value)
    else:
        user_cell_range = list(range(last_read_row + 1, total_rows + 2))
        for i in range(last_read_row + 1, total_rows + 2):
            github_user_list.append(sheet.cell(i, 5).value)


def updating_google_sheet():
    getting_github_user_list()
    for i in range(len(github_user_list)):
        if github_user_list[i] == "":
            # to insert the data in the google sheet that no github profile provided
            sheet.update_cell(user_cell_range[i], 12, 0)
        else:
            github_api = f"https://api.github.com/users/{github_user_list[i][19:]}/repos"
            r = requests.get(github_api)
            r = r.json()
            r_java = [
                dict_result for dict_result in r if dict_result['language'] == 'Python']
            sheet.update_cell(user_cell_range[i], 12, len(r_java))
    print("Python file: All the Github repos for the pending rows have been identified and necessary data has been inserted")


if last_read_row == total_rows:
    print("Python file: You have already read and updated all the rows")
else:
    updating_google_sheet()
