from scraper.scraper import get_hyperlink
from scraper.navigator import navigate_to_hyperlink
from config import BASE_URL, CHROME_DRIVER_PATH

if __name__ == "__main__":
    hyperlink = get_hyperlink(BASE_URL)
    if hyperlink:
        print(f"Found hyperlink: {hyperlink}")
        navigate_to_hyperlink(BASE_URL, hyperlink, CHROME_DRIVER_PATH)
    else:
        print("No hyperlink found!")
