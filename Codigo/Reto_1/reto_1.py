from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
import gspread

#Function for cleaning the cells in the worksheet
def clean_sheet(worksheet):
    range_of_cells = worksheet.range('A1:Z1000')
    for cell in range_of_cells:
        cell.value = ''
    worksheet.update_cells(range_of_cells)

SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

SERVICE_ACCOUNT_FILE = 'keys.json'
creds = None
creds  = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#Spredsheet config
SAMPLE_SPREADSHEET_ID_SOURCE = '1DRD97TAw2WIuTCG0Nh6BW-aVvDKAgY1wvJb38V-3vU8'
SAMPLE_SPREADSHEET_ID_RESULT = '1LhXACLLONdBOnouab2BH536SXVifg9gvWRqbM-UPYwA'

service = build('sheets', 'v4', credentials=creds)
# Calling the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_SOURCE,range="Reto1!A1:D16").execute()

values = result.get('values', [])
headers = values.pop(0) #Data cleaning
df=pd.DataFrame(values,columns=headers)
#print(df)

#Creating Pivot Table
tb_pivot_1 = pd.pivot_table(df,index=["Author","Sentiment"], columns= {'Country':["Country"]},values="Theme",fill_value="FALSO",aggfunc=lambda x: 'VERDADERO')
tb_pivot_2=pd.pivot_table(df,index=["Author","Sentiment"], columns={'Theme':["Theme"]},values="Country",fill_value="FALSO",aggfunc=lambda x: 'VERDADERO')
index_1 = tb_pivot_1.index
tb_pivot_1.name = "Country"
index_2 = tb_pivot_1.index
tb_pivot_2.name = "Theme"
print(tb_pivot_1)
print(tb_pivot_2)

#Merging pivot tables
tb_pivot = pd.merge(tb_pivot_1, tb_pivot_2, 'left', on = ["Author","Sentiment"])
print(tb_pivot)

#Appending info to the spreedsheet
gc = gspread.service_account(filename='keys.json')
sh = gc.open_by_key(SAMPLE_SPREADSHEET_ID_RESULT)
worksheet = sh.get_worksheet(0)
clean_sheet(worksheet)
worksheet.update('C1:K1','Country')
worksheet.update('L1:R1','Theme')
worksheet.update('A2',"Author")
worksheet.update('B2',"Sentiment")
worksheet.update('A3',tb_pivot.index.tolist())
worksheet.update('C2',[tb_pivot.columns.values.tolist()] +(tb_pivot.values.tolist()))
#set_with_dataframe(worksheet, tb_pivot)




