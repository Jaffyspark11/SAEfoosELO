import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# connect to google drive and sheets

myscope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

mycreds = ServiceAccountCredentials.from_json_keyfile_name("mycreds.json", myscope)
myclient = gspread.authorize(mycreds)

spreadsheet = myclient.open("Foos Elo")

gameResults = spreadsheet.sheet1

rows1 = gameResults.get("A:F")

results_df = pd.DataFrame(rows1[1:], columns=rows1[0])


playerNames = spreadsheet.get_worksheet(1)

rows2 = playerNames.get("A:D")

ratings_df = pd.DataFrame(rows2[1:], columns=rows2[0])


print(results_df)
