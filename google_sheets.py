"""
Google Sheets integration module for the Cryptocurrency Listing Scraper.
Handles all interactions with Google Sheets API including updates and modifications.
"""
import gspread
from typing import List
from google.oauth2.service_account import Credentials

def append_empty_row_google_sheet(sheet_name: str, sheet_num: int, credentials_file: str = "credentials.json") -> None:
    """
    Adds an empty row to a specified Google Sheet.

    Args:
        sheet_name (str): Name of the target Google Sheet
        sheet_num (int): Sheet index number (1-based)
        credentials_file (str): Path to Google Service Account credentials

    Returns:
        None

    Raises:
        gspread.exceptions.APIError: For API-related errors
        FileNotFoundError: If credentials file is missing
    """
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    # Authenticate with Google Sheets API
    creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
    client = gspread.authorize(creds)

    # Open the sheet
    sheet = client.open(sheet_name).get_worksheet(sheet_num-1)
    data = [
        "==== Reached Maximum Number of Rows to Extract. " +
        "==== Fill in Missing Rows Here.. ===="
    ]

    # Add 1 row to the sheet
    sheet.insert_row(data,2)
    print("Added row in Google Sheet table successfully.")


def update_google_sheet(sheet_name: str, sheet_num: int, data: List[List[str]], credentials_file: str = "credentials.json") -> None:
    """
    Updates a Google Sheet with new cryptocurrency data.

    Args:
        sheet_name (str): Name of the target Google Sheet
        sheet_num (int): Sheet index number (1-based)
        data (List[List[str]]): Data to insert, each inner list is one row
        credentials_file (str): Path to Google Service Account credentials

    Returns:
        None

    Raises:
        gspread.exceptions.APIError: For API-related errors
        FileNotFoundError: If credentials file is missing
    """
    # Define the required scopes
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    # Authenticate with Google Sheets API
    creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).get_worksheet(sheet_num-1)
    sheet.insert_rows(data,2)
    print("Google Sheet table updated successfully.")
