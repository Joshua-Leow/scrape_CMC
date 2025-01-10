from google_sheets import update_google_sheet
from scraper.scraper import *
from config import BASE_URL, CHROME_DRIVER_PATH
from scraper.scraper import get_data_from_hyperlink

if __name__ == "__main__":
    # Use the Service class to specify the ChromeDriver path
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.get(BASE_URL)

    hyperlinks = get_hyperlinks(BASE_URL) # List of hyperlinks
    driver.quit()

    if not hyperlinks:
        print("There are no new listings in Coin Market Cap")
        exit()

    rows_to_update=[] # List of lists to store rows to be added to Google Sheet Table
    for link in hyperlinks[::-1]:
        rows_to_update.append(get_data_from_hyperlink(BASE_URL, link, CHROME_DRIVER_PATH))

    # Update Google Sheets
    update_google_sheet(
        sheet_name="CMC_new",
        data=rows_to_update,
        credentials_file=os.path.join(os.path.dirname(__file__), "credentials.json"),
    )

