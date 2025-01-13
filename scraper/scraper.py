import re

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
        try:
            if driver.find_element(By.CSS_SELECTOR, NO_DATA_TEXT).is_displayed():
                print("fail at NO_DATA_TEXT displayed")
                return None
        except:
            pass
        num_rows = len(driver.find_elements(By.CSS_SELECTOR, "table.cmc-table > tbody > tr"))
        print(f"num_rows: {num_rows}")
        exchanges = []
        for i in range(2,num_rows+1):
            EXCHANGE_TARGET = replace_str_index(MARKET_TITLE_TEXT, 39, str(i))
            exchange_element = driver.find_element(By.CSS_SELECTOR, EXCHANGE_TARGET)
            if exchange_element:
                exchange_data = exchange_element.text
                # print(f"exchange data: {exchange_data}")
                if all_exchange:
                    exchange_data, vol_perc_float = get_vol_perc(driver, i, exchange_data)
                if exchange_data:
                    exchanges.append(exchange_data)
                    # print(f"exchanges list: {exchanges}")
            else:
                break
        sorted_exchanges = sorted(list(set(exchanges)), key=extract_percentage, reverse=True)
        sorted_exchanges = ", ".join(sorted_exchanges)
        print(f"List of sorted exchanges are: {sorted_exchanges}")
    except Exception as e:
        print("fail at get_exchange exception")
        print(e)
        return None
    return sorted_exchanges

def get_cex_exchange(driver):
    try:
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, SHOW_CEX_BUTTON))
        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CSS_SELECTOR, "#section-coin-markets > section > div > div:nth-child(1) > p"))
        driver.implicitly_wait(1)
        exchanges = get_exchange(driver, all_exchange=False)
    except Exception as e:
        print("fail at get_cex_exchange exception")
        print(e)
        return None
    return exchanges

def get_dex_exchange(driver):
    try:
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, SHOW_DEX_BUTTON))
        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CSS_SELECTOR, "#section-coin-markets > section > div > div:nth-child(1) > p"))
        driver.implicitly_wait(1)
        exchanges = get_exchange(driver, all_exchange=False)
    except Exception as e:
        print("fail at get_dex_exchange exception")
        print(e)
        return None
    return exchanges

def get_notes(soup):
    try:
        about_notes_target = soup.select_one(ABOUT_TEXT)
        about_notes = about_notes_target.get_text() if about_notes_target else None
    except Exception as e:
        print(e)
        return None
    return about_notes

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

def get_x_link(soup):
    try:
        X_link = None
        for i in range(1,4):
            X_TARGET = replace_str_index(SOCIALS_LINKS, -6, str(i))
            x_element = soup.select_one(X_TARGET)
            if x_element["href"]:
                X_link = x_element["href"]
                X_link = "https:" + X_link
                if "twitter.com" in X_link:
                    return X_link
    except Exception as e:
        print(e)
        return None
    return X_link

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


def get_data_from_hyperlink(base_url, hyperlink, driver_path):
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
        tags = get_tags(soup)
        # selenium open browser
        driver.get(base_url[:-4] + hyperlink)
        exchange, cex_exchange, dex_exchange = "", "", ""
        try:
            coin_markets_element = driver.find_element(By.ID, "section-coin-markets")
            driver.execute_script("arguments[0].scrollIntoView();", coin_markets_element)
            WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CSS_SELECTOR, MARKET_TITLE_TEXT))
            exchange = get_exchange(driver)
            # dex_exchange = get_dex_exchange(driver)
            cex_exchange = get_cex_exchange(driver)
        except Exception as e:
            print("Failed to get exchange data")
            print(e)
        driver.quit()
        stage = "Prospect"
        est_value = 30000
        contact = "rep@example.com"
        predicted_probability = get_predicted_probability()
        website = get_website(soup)
        X_link = get_x_link(soup)
        notes = get_notes(soup)
        source = url
        impt = get_important(soup)

        result = [
            name,
            tags,
            exchange,
            # dex_exchange,
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
        pass

    return result
