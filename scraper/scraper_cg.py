import re
import os
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from config import MAX_ROWS
from scraper.pages_cg import *

def replace_str_index(text,index=0,replacement=''):
    return f'{text[:index]}{replacement}{text[index+1:]}'

def read_last_hyperlink_cg():
    script_dir = os.path.dirname(__file__)
    rel_path = "../data/last_hyperlink_cg.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    # Read the last hyperlink if the file exists
    last_hyperlink = None
    try:
        with open(abs_file_path, "r") as file:
            last_hyperlink = file.read().strip()
            print(f"Current link in last_hyperlink.txt is: {last_hyperlink}")
    except Exception as e:
        print(f"Failed to locate last_hyperlink.txt file in path: [{abs_file_path}]")
        print(e)
    return last_hyperlink

def read_CG_table():
    script_dir = os.path.dirname(__file__)
    rel_path = "../data/CG_table.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    # Read the last hyperlink if the file exists
    cg_table = None
    try:
        with open(abs_file_path, "r") as file:
            cg_table = file.read().strip()
            print(f"cg_table in cg_table.txt is: {cg_table[:100]}")
    except Exception as e:
        print(f"Failed to locate cg_table.txt file in path: [{abs_file_path}]")
        print(e)
    return cg_table

def get_time(table, i):
    time_selector = f"tr:nth-child({i}) > td:nth-child(11)"
    time_text = table.select_one(time_selector).text
    ini_time_for_now = datetime.now() - timedelta(minutes=i)
    time, num = None, None
    time_text_list = time_text.split()
    for time_text in time_text_list:
        try:
            num = int(time_text)
            break
        except:
            pass
    try:
        if time_text_list[-1] == 'minutes' or time_text_list[-1] == 'minute':
            time = ini_time_for_now - timedelta(minutes=num)
        elif time_text_list[-1] == 'hours' or time_text_list[-1] == 'hour':
            time = ini_time_for_now - timedelta(hours=num)
        elif time_text_list[-1] == 'days' or time_text_list[-1] == 'day':
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
        return hyperlink  # Stop if the hyperlink matches last_hyperlink.txt

    return hyperlink

def get_hyperlinks_time_cg():
    hyperlinks_time, first_hyperlink = [], None
    CG_table = read_CG_table()
    last_hyperlink = read_last_hyperlink_cg()
    max_rows = MAX_ROWS if last_hyperlink else 1  # Limit rows based on the file existence

    # Fetch the webpage
    soup = BeautifulSoup(CG_table, "html.parser")
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

def get_coin_name(driver):
    coin_name = driver.find_element(By.CSS_SELECTOR, COIN_NAME_TEXT).text
    # print(f"coin_name is: {coin_name}")
    return coin_name

def get_coin_symbol(driver):
    coin_symbol = driver.find_element(By.CSS_SELECTOR, COIN_SYMBOL_TEXT).text
    if coin_symbol[-6:] == ' Price':
        coin_symbol = coin_symbol[:-6]
    # print(f"coin_symbol is: {coin_symbol}")
    return coin_symbol

def get_mcap(driver):
    mcap = driver.find_element(By.CSS_SELECTOR, MARKET_CAP_TEXT).text
    # print(f"mcap is: {mcap}")
    return mcap

def get_tags(driver):
    info_table_keys_elements = driver.find_elements(By.CSS_SELECTOR, INFO_TABLE_KEYS)
    info_table_keys = [elem.text for elem in info_table_keys_elements]
    for i, key in enumerate(info_table_keys):
        if 'Categories' in key:
            row = i
    TAGS_TARGET = replace_str_index(TAGS, 54, str(row+1))
    tags_str = ""
    try:
        tags_elements = driver.find_elements(By.CSS_SELECTOR, TAGS_TARGET)
        tags = [elem.text for elem in tags_elements]
        for i, tag in enumerate(tags):
            if 'Suggest a Category' in tag:
                tags.pop(i)
        tags_str = ", ".join(tags)
    except Exception as e: print(f"Failed at get_tags function.\n{e}")
    # print(f'tags_str is: {tags_str}')
    return tags_str

def get_vol_perc(driver, i, exchange_data):
    vol_perc_float = None
    VOL_PERC_TARGET = replace_str_index(VOL_PERC_TEXT, 39, str(i))
    vol_perc_text = driver.find_element(By.CSS_SELECTOR, VOL_PERC_TARGET).text
    # print(f"vol_perc_text is: {vol_perc_text}")
    if vol_perc_text != '--%':
        if vol_perc_text == '<0.01%':
            vol_perc_text = "0.01"
        exchange_data = exchange_data + "[" + vol_perc_text + "]"
    return exchange_data, vol_perc_float

def extract_percentage(item):
    match = re.search(r"\[(\d+\.?\d*)%]", item)  # Regex to extract percentage
    return float(match.group(1)) if match else -1  # Return -1 for items without percentage

def get_exchange(driver, all_exchange=True):
    pass

def get_notes(driver):
    about_more_button = driver.find_element(By.CSS_SELECTOR, ABOUT_MORE_BUTTON)
    driver.execute_script("arguments[0].scrollIntoView();", about_more_button)
    driver.execute_script("arguments[0].click();", about_more_button)
    about_text = driver.find_element(By.CSS_SELECTOR, ABOUT_TEXT).text.strip()
    # print(f"about_text is: {about_text}")
    return about_text

def get_website(driver):
    website = driver.find_element(By.CSS_SELECTOR, WEBSITE_LINK)
    website = website.get_attribute('href')
    # print(f"website is: {website}")
    return website

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

def get_predicted_probability():
    return 0.50

def get_data_from_hyperlink_cg(base_url, hyperlink, driver_path):
    service = Service(driver_path)
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(service=service, options=options)
    try:
        url = base_url + hyperlink
        driver.get(url)
        print(f"  Navigated to: {url}")
    except Exception as e: print(f"Failed to navigate to {base_url+hyperlink}\n{e}")
    try:
        name = get_coin_name(driver) + " (" + get_coin_symbol(driver) + ")"
        mcap = get_mcap(driver)
        website = get_website(driver)
        X_link = get_x_link(driver)
        notes = get_notes(driver)
        tags = get_tags(driver)
        # exchange = get_exchange(driver)
    except Exception as e:
        print(f"Failed to get exchange data\n{e}")
    # selenium open browser
    exchange, cex_exchange, dex_exchange = "", "", ""
    driver.quit()

    stage = "Prospect"
    est_value = 30000
    contact = "rep@example.com"
    predicted_probability = get_predicted_probability()
    # source = url
    # impt = ""
    # impt = get_important(soup)

    result = None
    # result = [
    #     name,
    #     mcap,
    #     tags,
    #     exchange,
    #     # dex_exchange,
    #     cex_exchange,
    #     stage,
    #     est_value,
    #     contact,
    #     predicted_probability,
    #     website,
    #     X_link,
    #     notes,
    #     source,
    #     impt
    # ]

    return result
