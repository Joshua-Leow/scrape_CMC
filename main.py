from genai import *
from google_sheets import update_google_sheet, append_empty_row_google_sheet
from scraper.scraper import *
from config import BASE_URL, CHROME_DRIVER_PATH
from scraper.scraper import get_data_from_hyperlink

if __name__ == "__main__":
    hyperlinks_time = get_hyperlinks_time(BASE_URL) # List of tuple (hyperlinks, time)
    if not hyperlinks_time:
        print("There are no new listings in Coin Market Cap")
        exit()

    rows_to_update=[] # List of lists to store rows to be added to Google Sheet Table
    for link_time_tuple in hyperlinks_time:
        result = get_data_from_hyperlink(BASE_URL, link_time_tuple[0], CHROME_DRIVER_PATH)
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

