from datetime import datetime, timedelta
import os
from bs4 import BeautifulSoup

from config import MAX_ROWS

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
