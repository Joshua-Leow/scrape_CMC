import gspread
from google.oauth2.service_account import Credentials

def append_empty_row_google_sheet(sheet_name, credentials_file="credentials.json"):
    """
    Adds an empty row in Google Sheet table.

    :param sheet_name: Name of the Google Sheet.
    :param credentials_file: Path to the Google Service Account JSON file.
    """
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    # Authenticate with Google Sheets API
    creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
    client = gspread.authorize(creds)

    # Open the sheet
    sheet1 = client.open(sheet_name).sheet1
    data = [
        "==== Reached Maximum Number of Rows to Extract. " +
        "==== Fill in Missing Rows Here.. ===="
    ]

    # Add 1 row to the sheet
    sheet1.insert_row(data,2)

# TODO: format cells will cause future cells inserted to also be formatted
    # # Color the background of 'A2:B2' cell range in black,
    # # change horizontal alignment, text color and font size
    # sheet1.format("A2:B2", {
    #     "wrapStrategy": "OVERFLOW_CELL",
    #     "backgroundColor": {
    #         "red": 0.0,
    #         "green": 0.0,
    #         "blue": 0.0
    #     },
    #     "horizontalAlignment": "CENTER",
    #     "textFormat": {
    #         "foregroundColor": {
    #             "red": 1.0,
    #             "green": 1.0,
    #             "blue": 1.0
    #         },
    #         "fontSize": 12,
    #         "bold": True
    #     }
    # })

    print("Added row in Google Sheet table successfully.")

def update_google_sheet(sheet_name, data, credentials_file="credentials.json"):
    """
    Updates a Google Sheet table with web scraping data.

    :param sheet_name: Name of the Google Sheet.
    :param data: List of lists, each representing one row of data to add.
    :param credentials_file: Path to the Google Service Account JSON file.
    """
    # Define the required scopes
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    # Authenticate with Google Sheets API
    creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
    client = gspread.authorize(creds)

    # Open the sheet
    sheet1 = client.open(sheet_name).sheet1
    # sheet2 = client.open(sheet_name).get_worksheet(1)

    # Append rows to the sheet
    for row in data:
        print(f"Inserted row {row} into Google Sheet.")
        sheet1.insert_row(row,2)

    print("Google Sheet table updated successfully.")
