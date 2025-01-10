# config.py

# Target website and headers for requests
BASE_URL = "https://coinmarketcap.com/new"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Path to WebDriver
CHROME_DRIVER_PATH = "resources/chromedriver-mac-arm64/chromedriver"

# Max rows to extract each run
MAX_ROWS = 10