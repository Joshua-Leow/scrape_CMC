from scraper.scraper import *
from scraper.navigator import *
from config import BASE_URL, CHROME_DRIVER_PATH

if __name__ == "__main__":
    # Use the Service class to specify the ChromeDriver path
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.get(BASE_URL)

    hyperlinks = get_hyperlinks(BASE_URL)
    driver.quit()

    for link in hyperlinks:
        navigate_to_hyperlink(BASE_URL, link, CHROME_DRIVER_PATH)
