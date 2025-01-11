from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

from config import MAX_ROWS
from scraper.pages import *
import os

def replace_str_index(text,index=0,replacement=''):
    return f'{text[:index]}{replacement}{text[index+1:]}'

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
    max_rows = MAX_ROWS if last_hyperlink else 1  # Limit rows based on the file existence

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


def get_coin_name(soup):
    coin_name_target = soup.select_one(COIN_NAME_TEXT)
    coin_name = coin_name_target.get_text()[:-6] if coin_name_target else None
    return coin_name

def get_coin_symbol(soup):
    coin_symbol_target = soup.select_one(COIN_SYMBOL_TEXT)
    coin_symbol = coin_symbol_target.get_text() if coin_symbol_target else None
    return coin_symbol

def get_tags(soup):
    tags = ""
    for i in range(1,4):
        TAG_TARGET = replace_str_index(TAGS, -6, str(i))
        tag_target = soup.select_one(TAG_TARGET)
        tag = tag_target.get_text() if tag_target else None
        if tag:
            tags = tags + ", " + tag
    tags = tags[2:] if tags else tags
    tags = tags+", (and more)" if soup.select_one(SHOW_ALL_TAGS_BUTTON) else tags
    return tags

def get_exchange(soup, driver):
    # if soup.select_one(NO_DATA_TEXT): return None
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.cmc-table > tbody"))
    )
    exchanges = ""
    for i in range(2,11):
        EXCHANGE_TARGET = replace_str_index(MARKET_TITLE_TEXT, 39, str(i))
        exchange_target = soup.select_one(EXCHANGE_TARGET)
        print(f"exchange_target is: {exchange_target}")
        vol_perc_target = soup.select_one(VOL_PERC_TEXT)
        exchanges = []
        if exchange_target:
            exchange_data = exchange_target.get_text()
            if vol_perc_target:
                exchange_data = exchange_data + " (" + vol_perc_target.get_text() + ")"
            if exchange_data:
                exchanges.append(exchange_data)
        else:
            break
    exchanges = ", ".join(list(set(exchanges)))
    return exchanges

def get_notes(soup):
    about_notes_target = soup.select_one(ABOUT_TEXT)
    about_notes = about_notes_target.get_text() if about_notes_target else None
    return about_notes

def get_website(soup):
    website_target = soup.select_one(WEBSITE_LINK)
    website = website_target["href"] if website_target else None
    return website


def get_predicted_probability():
    return 0.50


def get_data_from_hyperlink(base_url, hyperlink, driver_path):
    # Use the Service class to specify the ChromeDriver path
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    try:
        url = base_url[:-4] + hyperlink
        # driver.get(base_url[:-4] + hyperlink)

        # Fetch the webpage
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        print(f"  Navigated to: {url}")

        name = get_coin_name(soup) + " (" + get_coin_symbol(soup) + ")"
        tags = get_tags(soup)
        # selenium open browser
        driver.get(base_url[:-4] + hyperlink)
        exchange = get_exchange(soup, driver)
        driver.quit()
        stage = "Prospect"
        est_value = 30000
        contact = "rep@example.com"
        predicted_probability = get_predicted_probability()
        website = get_website(soup)
        X_link = ""
        notes = get_notes(soup)
        source = url

        result = [
            name,
            tags,
            exchange,
            stage,
            est_value,
            contact,
            predicted_probability,
            website,
            X_link,
            notes,
            source
        ]
    finally:
        pass

    return result
