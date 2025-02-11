import re
import os
import time
from typing import List, Tuple, Optional
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service

from config import MAX_ROWS
from scraper.pages_cmc import *

def replace_str_index(text,index=0,replacement=''):
    return f'{text[:index]}{replacement}{text[index+1:]}'

def read_last_hyperlink():
    script_dir = os.path.dirname(__file__)
    rel_path = "../data/last_hyperlink_cmc.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    # Read the last hyperlink if the file exists
    last_hyperlink = None
    try:
        with open(abs_file_path, "r") as file:
            last_hyperlink = file.read().strip()
            print(f"Current link in last_hyperlink_cmc.txt is: {last_hyperlink}")
    except Exception as e:
        print(f"Failed to locate last_hyperlink_cmc.txt file in path: [{abs_file_path}]")
        print(e)
    return last_hyperlink

def overwrite_last_hyperlink(first_hyperlink, source):
    script_dir = os.path.dirname(__file__)
    rel_path = "../data/last_hyperlink_"+ str(source).lower() +".txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    # Update the last_hyperlink_cmc.txt file with the first hyperlink
    if first_hyperlink:
        with open(abs_file_path, "w") as file:
            file.write(first_hyperlink)
            print(f"Updated link in last_hyperlink_cmc.txt to: {first_hyperlink}")


def get_time(table, i):
    time_selector = f"tr:nth-child({i}) > td:nth-child(10)"
    time_text = table.select_one(time_selector).text
    ini_time_for_now = datetime.now() - timedelta(minutes=i)
    time = None
    try:
        num = int(time_text.split()[0])
        if time_text[-11:] == 'minutes ago' or time_text[-10:] == 'minute ago':
            time = ini_time_for_now - timedelta(minutes=num)
        elif time_text[-9:] == 'hours ago' or time_text[-8:] == 'hour ago':
            time = ini_time_for_now - timedelta(hours=num)
        elif time_text[-8:] == 'days ago' or time_text[-7:] == 'day ago':
            time = ini_time_for_now - timedelta(days=num)
        time = time.strftime("%Y-%m-%d %H:%M")
    except Exception as e:
        print(f"Failed to get time. time_text is: {time_text}")
        print(e)
    return time

def get_link(table, i, last_hyperlink):
    link_selector = f"tr:nth-child({i}) > td:nth-child(3) > a"
    link_tag = table.select_one(link_selector)
    hyperlink = None
    try:
        hyperlink = link_tag["href"]
    except Exception as e:
        print(f"Failed to get link tag href hyperlink. link_tag is: {link_tag}")
        print(e)
    if hyperlink == last_hyperlink:
        return hyperlink  # Stop if the hyperlink matches last_hyperlink_cmc.txt

    return hyperlink

def get_hyperlinks_time_cmc(base_url: str) -> Tuple[List[Tuple[str, str]], Optional[str]]:
    """
    Retrieves new cryptocurrency listing URLs and their timestamps.

    Args:
        base_url (str): Base URL of the cryptocurrency listing platform

    Returns:
        Tuple containing:
        - List of tuples (hyperlink, timestamp)
        - First hyperlink found (for progress tracking)

    Raises:
        requests.exceptions.RequestException: For network-related errors
        ValueError: If required elements aren't found
    """
    hyperlinks_time, first_hyperlink = [], None
    last_hyperlink = read_last_hyperlink()
    max_rows = MAX_ROWS if last_hyperlink else 1  # Limit rows based on the file existence

    # Fetch the webpage
    response = requests.get(base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    # Locate the table
    table_selector = "table > tbody"
    table = soup.select_one(table_selector)
    if not table: raise ValueError("Table not found on the webpage")

    for i in range(1, max_rows + 1):
        hyperlink = get_link(table, i, last_hyperlink)
        time = get_time(table, i)
        if i == 1:
            first_hyperlink = hyperlink
        if hyperlink == last_hyperlink:
            break
        hyperlinks_time.append((hyperlink,time))
        print(f"Row {i} hyperlink is: {hyperlink}")
        print(f"      time is: {time}")

    return hyperlinks_time, first_hyperlink

def get_coin_name(soup):
    try:
        coin_name_target = soup.select_one(COIN_NAME_TEXT)
        coin_name = coin_name_target.get_text()[:-6] if coin_name_target else None
    except Exception as e:
        print(e)
        return None
    return coin_name

def get_coin_symbol(soup):
    try:
        coin_symbol_target = soup.select_one(COIN_SYMBOL_TEXT)
        coin_symbol = coin_symbol_target.get_text() if coin_symbol_target else None
    except Exception as e:
        print(e)
        return None
    return coin_symbol

def get_mcap(soup):
    try:
        market_cap_target = soup.select_one(MARKET_CAP_TEXT)
        market_cap = market_cap_target.get_text() if market_cap_target else None
    except Exception as e:
        print(e)
        return None
    return market_cap

def get_tags(soup):
    tags = ""
    try:
        for i in range(1,4):
            TAG_TARGET = replace_str_index(TAGS, -6, str(i))
            tag_target = soup.select_one(TAG_TARGET)
            tag = tag_target.get_text() if tag_target else None
            if tag:
                tags = tags + ", " + tag
        tags = tags[2:] if tags else tags
        tags = tags+", (and more)" if soup.select_one(SHOW_ALL_TAGS_BUTTON) else tags
    except Exception as e:
        print(e)
        return None
    return tags

def get_vol_perc(driver, i, exchange_data):
    vol_perc_float = None
    VOL_PERC_TARGET = replace_str_index(VOL_PERC_TEXT, 39, str(i))
    vol_perc_text = driver.find_element(By.CSS_SELECTOR, VOL_PERC_TARGET).text
    # print(f"vol_perc_text is: {vol_perc_text}")
    if vol_perc_text != '--%':
        if vol_perc_text == '<0.01%':
            vol_perc_text = "0.01"
        # else:
        #     try:
        #         vol_perc_float = float(vol_perc_text[:-1])
        #     except Exception as e:
        #         print(e)
        exchange_data = exchange_data + "[" + vol_perc_text + "]"
    return exchange_data, vol_perc_float

def extract_percentage(item):
    match = re.search(r"\[(\d+\.?\d*)%]", item)  # Regex to extract percentage
    return float(match.group(1)) if match else -1  # Return -1 for items without percentage

def get_exchange(driver, all_exchange=True):
    try:
        if all_exchange:
            WebDriverWait(driver, 5).until(lambda x: x.find_element(By.ID, "section-coin-markets"))
            coin_markets_element = driver.find_element(By.ID, "section-coin-markets")
            driver.execute_script("arguments[0].scrollIntoView();", coin_markets_element)
        time.sleep(2)

        num_rows = len(driver.find_elements(By.CSS_SELECTOR, "table.cmc-table > tbody > tr"))
        # print(f"num_rows: {num_rows}")
        exchanges = []
        for i in range(1,num_rows+1):
            EXCHANGE_TARGET = replace_str_index(MARKET_TITLE_TEXT, 28, ":nth-child(" + str(i) + ") ")
            try:
                exchange_element = driver.find_element(By.CSS_SELECTOR, EXCHANGE_TARGET)
                exchange_data = exchange_element.text
                if all_exchange:
                    exchange_data, vol_perc_float = get_vol_perc(driver, i, exchange_data)
                exchanges.append(exchange_data)
                # print(f"exchanges list: {exchanges}")
            except:
                if driver.find_element(By.CSS_SELECTOR, NO_DATA_TEXT).is_displayed():
                    return None
                else: print(f"failed to locate EXCHANGE_TARGET: {EXCHANGE_TARGET}")
        sorted_exchanges = sorted(list(set(exchanges)), key=extract_percentage, reverse=True)
        sorted_exchanges = ", ".join(sorted_exchanges)
        # print(f"List of sorted exchanges are: {sorted_exchanges}")

    except Exception as e:
        print(f"fail at get_exchange exception\n{e}")
        return None
    return sorted_exchanges

def get_cex_exchange(driver):
    try:
        WebDriverWait(driver, 5).until(lambda x: x.find_element(By.CSS_SELECTOR, SHOW_CEX_BUTTON))
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, SHOW_CEX_BUTTON))
        exchanges = get_exchange(driver, all_exchange=False)
    except Exception as e:
        print("fail at get_cex_exchange exception")
        print(e)
        return None
    return exchanges

def get_dex_exchange(driver):
    try:
        WebDriverWait(driver, 5).until(lambda x: x.find_element(By.CSS_SELECTOR, SHOW_DEX_BUTTON))
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, SHOW_DEX_BUTTON))
        exchanges = get_exchange(driver, all_exchange=False)
    except Exception as e:
        print("fail at get_dex_exchange exception")
        print(e)
        return None
    return exchanges

def get_x_link(driver):
    X_link = ""
    try:
        social_elements = driver.find_elements(By.CSS_SELECTOR, SOCIALS_LINKS)
        social_links = [elem.get_attribute('href') for elem in social_elements]
        for link in social_links:
            if 'twitter.com' in link:
                X_link = link
        if len(social_links) > 0:
            X_link = social_links[0]
    except Exception as e:
        print(f"Failed at X link function.\n{e}")
    # print(f'X_link is: {X_link}')
    return X_link

def get_website(soup):
    try:
        website_target = soup.select_one(WEBSITE_LINK)
        if website_target["href"]:
            website = website_target["href"]
            website = "https:" + website
        else:
            return None
    except Exception as e:
        print(e)
        return None
    return website

def get_notes(soup):
    try:
        about_notes_target = soup.select_one(ABOUT_TEXT)
        about_notes = about_notes_target.get_text() if about_notes_target else None
    except Exception as e:
        print(e)
        return None
    return about_notes

def get_predicted_probability():
    return 0.50

def get_important(soup):
    try:
        important_target = soup.select_one(IMPORTANT_TEXT)
        important_text = important_target.get_text() if important_target else None
    except Exception as e:
        print(e)
        return None
    return important_text


def get_data_from_hyperlink(base_url: str, hyperlink: str, driver_path: str) -> List[str]:
    """
    Extracts detailed information about a cryptocurrency from its listing page.

    Args:
        base_url (str): Base URL of the cryptocurrency platform
        hyperlink (str): Specific URL path for the cryptocurrency
        driver_path (str): Path to ChromeDriver executable

    Returns:
        List containing extracted data in the following order:
        [name, market_cap, tags, exchanges, cex_exchanges, stage, value,
         contact, probability, website, social_link, description, source]

    Raises:
        selenium.common.exceptions.WebDriverException: For browser automation errors
        ValueError: If required data cannot be extracted
    """
    # Use the Service class to specify the ChromeDriver path
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    try:
        url = base_url[:-4] + hyperlink
        driver.get(base_url[:-4] + hyperlink)

        # Fetch the webpage
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        print(f"  Navigated to: {url}")

        name = get_coin_name(soup) + " (" + get_coin_symbol(soup) + ")"
        mcap = get_mcap(soup)
        tags = get_tags(soup)
        # selenium open browser
        driver.get(base_url[:-4] + hyperlink)
        exchange = get_exchange(driver)
        cex_exchange = get_cex_exchange(driver)
        X_link = get_x_link(driver)
        # end of selenium
        stage = "Prospect"
        est_value = 30000
        contact = "rep@example.com"
        predicted_probability = get_predicted_probability()
        website = get_website(soup)
        notes = get_notes(soup)
        source = url
        impt = get_important(soup)

        result = [
            name,
            mcap,
            tags,
            exchange,
            cex_exchange,
            stage,
            est_value,
            contact,
            predicted_probability,
            website,
            X_link,
            notes,
            source,
            impt
        ]
    finally:
        driver.quit()

    return result



