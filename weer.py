#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

try:
    # Start the driver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Load the weer.nl page for Amsterdam
        url = "https://www.weer.nl/noord-holland/amsterdam"
        driver.get(url)
        time.sleep(3)  # Wait for page to load

        # Get the rendered page source
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find the temperature span with class "text-temperature"
        temp_span = soup.find("span", class_="text-temperature")
        if temp_span:
            temp = temp_span.text.strip()  # e.g., "11°"
            print(f"{temp}")  # Outputs "11°"
        else:
            print("Not Found")

    finally:
        driver.quit()

except Exception:
    print("error")
