import gspread
from google.oauth2.service_account import Credentials

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
    sheet2 = client.open(sheet_name).get_worksheet(1)

    # Append rows to the sheet
    for row in data:
        sheet2.insert_row(row,2)
        # sheet2.append_row(row)

    print("Google Sheet table updated successfully.")
