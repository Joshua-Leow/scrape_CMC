from google_sheets import update_google_sheet
from scraper.scraper import *
from config import BASE_URL, CHROME_DRIVER_PATH
from scraper.scraper import get_data_from_hyperlink

if __name__ == "__main__":
    # Use the Service class to specify the ChromeDriver path
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.get(BASE_URL)

    hyperlinks = get_hyperlinks(BASE_URL)
    driver.quit()

    rows_to_update=[] # List of lists to store rows to be added to Google Sheet
    for link in hyperlinks:
        rows_to_update = get_data_from_hyperlink(rows_to_update, BASE_URL, link, CHROME_DRIVER_PATH) # List of lists to store rows to be added to Google Sheet

    # Update Google Sheets
    update_google_sheet(
        sheet_name="CMC_new",
        data=rows_to_update,
        credentials_file=os.path.join(os.path.dirname(__file__), "credentials.json"),
    )

