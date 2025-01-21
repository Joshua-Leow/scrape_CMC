"""
Main execution script for the Cryptocurrency Listing Scraper.
Coordinates the scraping of new cryptocurrency listings from multiple sources
and updates Google Sheets with the collected data.
"""
import os

from genai import gen_ai
from google_sheets import update_google_sheet, append_empty_row_google_sheet
from scraper.scraper_cg import get_hyperlinks_time_cg, get_data_from_hyperlink_cg
from scraper.scraper_cmc import get_hyperlinks_time_cmc, overwrite_last_hyperlink
from config import CMC_BASE_URL, CHROME_DRIVER_PATH, CG_BASE_URL, MAX_ROWS
from scraper.scraper_cmc import get_data_from_hyperlink

def main_cmc() -> None:
    """
    Main function for CoinMarketCap scraping process.

    Orchestrates the entire scraping workflow for CoinMarketCap:
    1. Retrieves new listing URLs and timestamps
    2. Extracts detailed information for each listing
    3. Processes and formats the data
    4. Updates Google Sheets
    5. Saves progress

    Returns:
        None

    Raises:
        Exception: For any critical errors during execution
    """
    hyperlinks_time, first_hyperlink = get_hyperlinks_time_cmc(CMC_BASE_URL) # List of tuple (hyperlinks, time)
    if not hyperlinks_time:
        print("There are no new listings in Coin Market Cap")
        return

    rows_to_update=[] # List of lists to store rows to be added to Google Sheet Table
    for link_time_tuple in hyperlinks_time:
        result = get_data_from_hyperlink(CMC_BASE_URL, link_time_tuple[0], CHROME_DRIVER_PATH)
        result.insert(0, link_time_tuple[1])
        result.insert(-2, gen_ai(result))
        rows_to_update.append(result)

    if len(hyperlinks_time) == MAX_ROWS:
        append_empty_row_google_sheet(sheet_name="New Cryptocurrencies", sheet_num=1)

    # Update Google Sheets
    update_google_sheet(
        sheet_name="New Cryptocurrencies",
        sheet_num=1,
        data=rows_to_update,
        credentials_file=os.path.join(os.path.dirname(__file__), "credentials.json"),
    )
    # overwrite last_hyperlink_cmc.txt with the first_hyperlink saved
    overwrite_last_hyperlink(first_hyperlink, "cmc")


def main_cg() -> None:
    """
    Main function for CoinGecko scraping process.

    Orchestrates the entire scraping workflow for CoinGecko:
    1. Retrieves new listing URLs and timestamps
    2. Extracts detailed information for each listing
    3. Processes and formats the data
    4. Updates Google Sheets
    5. Saves progress

    Returns:
        None

    Raises:
        Exception: For any critical errors during execution
    """
    hyperlinks_time, first_hyperlink = get_hyperlinks_time_cg()
    if not hyperlinks_time:
        print("There are no new listings in Coin Gecko")
        return

    rows_to_update=[] # List of lists to store rows to be added to Google Sheet Table
    for link_time_tuple in hyperlinks_time:
        result = get_data_from_hyperlink_cg(CG_BASE_URL, link_time_tuple[0], CHROME_DRIVER_PATH)
        result.insert(0, link_time_tuple[1])
        result.insert(-2, gen_ai(result))
        rows_to_update.append(result)

    if len(hyperlinks_time) == MAX_ROWS:
        append_empty_row_google_sheet(sheet_name="New Cryptocurrencies", sheet_num=2)

    # Update Google Sheets
    update_google_sheet(
        sheet_name="New Cryptocurrencies",
        sheet_num=2,
        data=rows_to_update,
        credentials_file=os.path.join(os.path.dirname(__file__), "credentials.json"),
    )
    # overwrite last_hyperlink_cmc.txt with the first_hyperlink saved
    overwrite_last_hyperlink(first_hyperlink, "cg")

if __name__ == "__main__":
    print("=== MAIN CMC STARTING ===")
    main_cmc()
    print("=== MAIN CMC COMPLETE ===")
    print("=== MAIN CG STARTING ===")
    main_cg()
    print("=== MAIN CG COMPLETE ===")
