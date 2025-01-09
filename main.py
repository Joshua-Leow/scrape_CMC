from scraper.scraper import *
from scraper.navigator import *
from config import BASE_URL, CHROME_DRIVER_PATH

if __name__ == "__main__":
    # Use the Service class to specify the ChromeDriver path
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.get(BASE_URL)
    print(f"Navigated to: {driver.current_url} [{driver.title}]")

    hyperlinks = get_hyperlinks(BASE_URL)
    print(f"list of hyperlinks: {hyperlinks}")
    driver.quit()

    for link in hyperlinks:
        print(f"link to navigate is : {BASE_URL[:-4] + link}")
        navigate_to_hyperlink(BASE_URL, link, CHROME_DRIVER_PATH)
