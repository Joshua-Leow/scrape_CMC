from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def navigate_to_hyperlink(base_url, hyperlink, driver_path):
    # Use the Service class to specify the ChromeDriver path
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    
    try:
        driver.get(base_url[:-4] + hyperlink)
        print(f"Navigated to: {driver.current_url}")
        
        # Optional: Print the title of the page
        print(f"Page Title: {driver.title}")
    
    finally:
        # Quit the driver to clean up
        driver.quit()
