from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from config import MAX_ROWS
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

def get_notes(soup):
    about_notes_target = soup.select_one(ABOUT_TEXT)
    about_notes = about_notes_target.get_text() if about_notes_target else None
    return about_notes

def get_predicted_probability():
    return 0.50


def get_data_from_hyperlink(base_url, hyperlink, driver_path):
    # Use the Service class to specify the ChromeDriver path
    # service = Service(driver_path)
    # driver = webdriver.Chrome(service=service)
    try:
        url = base_url[:-4] + hyperlink
        # driver.get(base_url[:-4] + hyperlink)

        # Fetch the webpage
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        print(f"  Navigated to: {url}")

        opportunity = get_coin_name(soup) + " (" + get_coin_symbol(soup) + ")"
        owner_email = "owner@example.com"
        stage = "Prospect"
        est_value = 30000
        rep_email = "rep@example.com"
        predicted_probability = get_predicted_probability()
        link = url
        notes = get_notes(soup)

        result = [
            opportunity,
            owner_email,
            stage,
            est_value,
            rep_email,
            predicted_probability,
            link,
            notes
        ]
    finally:
        pass

    return result