from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet. Please replace this text with the ID of your Google Sheet.
SAMPLE_SPREADSHEET_ID = '<PLEASE PUT IN THE ID OF YOUR SHEET>'
# Correlates to the all columns in the first 103 rows of the sheet. This might need to be changed
SAMPLE_RANGE_NAME = '!1:103'

def setup():
    # Initializes setup with Spreadsheet.

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    # Call the Sheets API and setups the sheet object
    sheet = service.spreadsheets()
    
    return sheet

def getStudentResponses(sheet):
    # Gets student responses and loads them into a list
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    
    # Filter values to grab just the cheat detection questions (marked with '***')
    question_indexes = []
    cell_count = 0
    for row in values:
        for cell in row:
            if (cell[:3] == '***'):
                question_indexes.append(cell_count)
            cell_count += 1
        # We just want to look at the first row on this iteration
        break

    # Populate a dictionary with the keys being student emails and responses being values
    student_responses = {}
    is_first = True
    for row in values:
        # Skip the first row because this doesn't include student data
        if (is_first == True):
            is_first = False
            continue
        cell_count = 0
        for cell in row:
            # Add Email as key
            if cell_count == 1:
                student_email = cell
                # Initialize value as empty list
                student_responses[cell] = []
            if cell_count > 1:
                for question_index in question_indexes:
                    if cell_count == question_index:
                        # Append the student response to the list of their responses
                        student_responses[student_email].append(cell)
            cell_count += 1

    return student_responses