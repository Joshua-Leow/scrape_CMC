from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from scraper.pages import *
import os

def get_hyperlink(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    # Select element using CSS selector
    hyperlink = soup.select_one(FIRST_HYPERLINK)
    return hyperlink["href"] if hyperlink else None

def get_hyperlinks(base_url):
    script_dir = os.path.dirname(__file__)
    rel_path = "../data/last_hyperlink.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    # Read the last hyperlink if the file exists
    last_hyperlink = None
    try:
        with open(abs_file_path, "r") as file:
            last_hyperlink = file.read().strip()
            print(f"Current link in last_hyperlink.txt is: {last_hyperlink}")
    except:
        print(f"Failed to locate last_hyperlink.txt file in path: [{abs_file_path}]")
    # Fetch the webpage
    response = requests.get(base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Locate the table
    table_selector = "table > tbody"
    table = soup.select_one(table_selector)
    if not table:
        raise ValueError("Table not found on the webpage")

    hyperlinks = []
    first_hyperlink = None
    max_rows = 10 if last_hyperlink else 2  # Limit rows based on the file existence

    for i in range(1, max_rows + 1):
        row_selector = f"tr:nth-child({i}) > td:nth-child(3) > a"
        link_tag = table.select_one(row_selector)

        if not link_tag or "href" not in link_tag.attrs:
            continue

        hyperlink = link_tag["href"]
        if i == 1:
            first_hyperlink = hyperlink  # Remember the first hyperlink

        if hyperlink == last_hyperlink:
            break  # Stop if the hyperlink matches last_hyperlink.txt

        hyperlinks.append(hyperlink)
        print(f"Row {i} link is: {hyperlink}")

    # Update the last_hyperlink.txt file with the first hyperlink
    if first_hyperlink:
        with open(abs_file_path, "w") as file:
            file.write(first_hyperlink)
            print(f"Updated link in last_hyperlink.txt to: {first_hyperlink}")

    return hyperlinks


def get_predicted_probability():
    return 0.50


def get_data_from_hyperlink(base_url, hyperlink, driver_path):
    # Use the Service class to specify the ChromeDriver path
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    try:
        driver.get(base_url[:-4] + hyperlink)
        print(f"  Navigated to: {driver.current_url}\n    Page Title: {driver.title}")
        predicted_probability = get_predicted_probability()
        owner_email = "owner@example.com"
        rep_email = "rep@example.com"
        result = [
            driver.title,
            owner_email,
            "Prospect",
            "$30 000",
            rep_email,
            predicted_probability,
            driver.current_url,
            "Scraped from CoinMarketCap",  # Example remark
        ]

    finally:
        driver.quit()

    return result