import os

from genai import gen_ai
from google_sheets import update_google_sheet, append_empty_row_google_sheet
from scraper.scraper_cg import get_hyperlinks_time_cg, get_data_from_hyperlink_cg
from scraper.scraper_cmc import get_hyperlinks_time, overwrite_last_hyperlink
from config import CMC_BASE_URL, CHROME_DRIVER_PATH, CG_BASE_URL, MAX_ROWS
from scraper.scraper_cmc import get_data_from_hyperlink

def main_cmc():
    hyperlinks_time, first_hyperlink = get_hyperlinks_time(CMC_BASE_URL) # List of tuple (hyperlinks, time)
    if not hyperlinks_time:
        print("There are no new listings in Coin Market Cap")
        exit()

    rows_to_update=[] # List of lists to store rows to be added to Google Sheet Table
    for link_time_tuple in hyperlinks_time:
        result = get_data_from_hyperlink(CMC_BASE_URL, link_time_tuple[0], CHROME_DRIVER_PATH)
        result.insert(0, link_time_tuple[1])
        result.insert(-2, gen_ai(result))
        rows_to_update.append(result)

    if len(hyperlinks_time) == MAX_ROWS:
        append_empty_row_google_sheet(sheet_name="CMC_new")
        # pass
    # Update Google Sheets
    update_google_sheet(
        sheet_name="CMC_new",
        data=rows_to_update,
        credentials_file=os.path.join(os.path.dirname(__file__), "credentials.json"),
    )
    # overwrite last_hyperlink.txt with the first_hyperlink saved
    overwrite_last_hyperlink(first_hyperlink)

def main_cg():
    hyperlinks_time, first_hyperlink = get_hyperlinks_time_cg()
    if not hyperlinks_time:
        print("There are no new listings in Coin Gecko")
        exit()

    rows_to_update=[] # List of lists to store rows to be added to Google Sheet Table
    for link_time_tuple in hyperlinks_time:
        result = get_data_from_hyperlink_cg(CG_BASE_URL, link_time_tuple[0], CHROME_DRIVER_PATH)
        result.insert(0, link_time_tuple[1])
        # result.insert(-2, gen_ai(result))
        rows_to_update.append(result)
    print(rows_to_update)


if __name__ == "__main__":
    # main_cmc()
    main_cg()