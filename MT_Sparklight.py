# Multithreading Sparklight scraper
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time
import random
import csv
import concurrent.futures


WaitTime = 5000
chunk = 10
in_file = "test_loading.csv"
out_file = "output.csv"
website = "https://www.sparklight.com/internet"

### SET UP BROWSER PREFERENCES
options = Options()
user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
options.set_preference("general.useragent.override", user_agent) # Set user agent to bypass website blocking
options.set_preference("dom.webdriver.enabled", False) # Disable webdriver mode to bypass website blocking

def load_page(driver):
    print("Waiting for page to load...")
    time.sleep(2)
    try:
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.ID, "css-loading")))
        print("Page loaded.")
    except TimeoutException:
        print("Page load timed out after 60 seconds.")
        return False

def search_address(address, zipCode, driver, wait, searchBar, zipCodeBar, searchButton, retries):
    if retries == 0:
        print("Retries exhausted. Skipping address...")
        return "website error, skipping address"
    
    searchBar.clear()
    zipCodeBar.clear()
    searchBar.send_keys(address)
    zipCodeBar.send_keys(zipCode)
    wait.until(EC.element_to_be_clickable(searchButton))
    searchButton.click()
    
    if (not load_page(driver, wait)) and retries > 0:
        print("Retrying search...")
        return search_address(address, zipCode, driver, wait, searchBar, zipCodeBar, searchButton, retries-1)

def process(data):
    driver = webdriver.Firefox(options=options)
    exception_occurred = False
    try:
        driver.get(website)
        wait = WebDriverWait(driver, 7)
        
        ### SEARCH AND SCRAPE
        for row in data[1:(chunk+1)]:
            address = ", ".join(row[2:5])
            zipCode = row[5]
            
            ### SEARCH KEY ELEMENTs
            searchBar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#update-address-comp-input-")))
            zipCodeBar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#update-zip-comp-input-")))
            searchButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#btn-update-address-comp-")))
                
            availability = search_address(address, zipCode, driver, wait, searchBar, zipCodeBar, searchButton, 3)
            row[7] = availability
            
    except Exception as e:
        exception_occurred = True
        print(f"Exception occurred: {e}")
    
    if exception_occurred:
        print(f"Thread failed. Retrying process...")
        driver.quit()
        return process(data) # Maybe delete later
    else:
        print("Thread completed")
        driver.quit()

    return data

### INITIALIZE MULTITHREADING
with open(in_file, "r") as file:
    reader = csv.reader(file)
    data = list(reader)
chunks = [data[i:i + chunk] for i in range(0, len(data), chunk)]
with concurrent.futures.ThreadPoolExecutor() as executor:
    processed_data = list(executor.map(process, chunks))
flattened_processed_data = [item for sublist in processed_data for item in sublist]
with open(out_file, "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerows(flattened_processed_data)
    