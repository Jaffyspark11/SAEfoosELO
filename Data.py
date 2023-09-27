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

worksheets = spreadsheet.worksheets()

gameResults = worksheets[0]

rows1 = gameResults.get_all_values()
print(rows1[0])

results_df = pd.DataFrame(rows1[1:], columns=rows1[0])


playerNames = worksheets[1]

rows2 = playerNames.get_all_values()

print(rows2[0])

ratings_df = pd.DataFrame(rows2[1:], columns=rows2[0])

for column in ratings_df.columns[1:]:
    ratings_df[column] = "1000"
    ratings_df[column].astype(float)


print(ratings_df)
