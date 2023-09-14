import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

#connect to google drive and sheets

myscope = ['https://spreadsheets.google.com/feeds',
           'https://www.googleapis.com/auth/drive']

mycreds = ServiceAccountCredentials.from_json_keyfile_name('mycreds.json', myscope)
myclient = gspread.authorize(mycreds)

spreadsheet = myclient.open("Foos Elo")

gameResults = spreadsheet.sheet1

rows1 = gameResults.get('A:F')

df1 = pd.DataFrame(rows1)

print(df1)