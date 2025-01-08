from bs4 import BeautifulSoup
import requests

def get_hyperlink(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Select element using CSS selector
    hypterlink = soup.select_one(
        "#__next > div.sc-f9c982a5-1.bVsWPX.global-layout-v2 > div > div.cmc-body-wrapper > div > div.sc-936354b2-2.iyOdZW > table > tbody > tr:nth-child(1) > td:nth-child(3) > a"
    )
    return hypterlink["href"] if hypterlink else None
