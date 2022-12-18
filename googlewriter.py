import httplib2
import string
import json
import datetime
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive']
COLUMNS = [['account_id', 'id', 'type', 'entity_id', 'entity_type', 'created_at', 'value_before', 'value_after']]
# SAMPLE_SPREADSHEET_ID = '1GmhnWWBbMGA5oLbzAtmhDvoLS3VF-XzQC-xkvdYr9cU' # spreadsheet_id
SAMPLE_SPREADSHEET_ID = '1ALiIpwVEm_fCUExvgZ27Lm8i6HEOx0XCXMihbdDK_eU'
SERVICE_ACCOUNT = "main-bot-371616-da676552f4ea.json" # Upload service account of Google Cloud


class GoogleWriter():

    def __init__(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT , SCOPES)
        httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
        self.service = build('sheets', 'v4', httpAuth) # Выбираем работу с таблицами и 4 версию API

        sheet = self.service.spreadsheets()
        first_values = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                          range="A1:H1").execute()
        
        if "values" not in first_values:
            self.service.spreadsheets().values().append(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range="A1:H1",
                body={
                    "values": COLUMNS
                },
                valueInputOption="USER_ENTERED"
            ).execute() # Checking empty or filled row
        
    def write(self, lst: list):
        """
        Write data in lst to GoogleSheets
        """
        if lst:
            self.service.spreadsheets().values().append(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range="Sheet1!A:Z",
                body={
                    "values": lst
                },
                valueInputOption="USER_ENTERED").execute()


class GoogleWriterV2():

    def __init__(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT , SCOPES)
        httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
        self.service = build('sheets', 'v4', httpAuth) # Выбираем работу с таблицами и 4 версию API

        sheet = self.service.spreadsheets()
        
        sheets_metadata = sheet.get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
        flag = False
        for i in range(len(sheets_metadata["sheets"])):
            if datetime.date.today().strftime("%B-%d-%Y") == sheets_metadata["sheets"][i]["properties"]["title"]:
                flag = True

        if flag == False:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                body={
                    "requests": [
                        {
                            "addSheet": {
                                "properties" : {
                                    "title" : datetime.date.today().strftime("%B-%d-%Y")
                                }
                            }
                        }
                    ]
                }
            ).execute()

        self.current_range = datetime.date.today().strftime("%B-%d-%Y") + "!A:Z"

        first_values = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                          range=self.current_range).execute()
        print(first_values)

        if "values" not in first_values:

            self.service.spreadsheets().values().append(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=self.current_range,
                body={
                    "values": COLUMNS
                },
                valueInputOption="USER_ENTERED"
            ).execute() # Checking empty or filled row
    
        

    def write(self, lst: list):
        """
        Write data in lst to GoogleSheets
        """
        if lst:
            self.service.spreadsheets().values().append(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=self.current_range,
                body={
                    "values": lst
                },
                valueInputOption="USER_ENTERED").execute()