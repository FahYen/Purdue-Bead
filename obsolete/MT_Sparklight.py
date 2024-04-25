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

AfterClickWaitTime = 5000
chunk = 10
in_file = "test3.csv"
out_file = "output.csv"
website = "https://www.sparklight.com/internet"

### SET UP BROWSER PREFERENCES
options = Options()
user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
options.set_preference("general.useragent.override", user_agent) # Set user agent to bypass website blocking
options.set_preference("dom.webdriver.enabled", False) # Disable webdriver mode to bypass website blocking

def wait_for_page_load(driver, timeout=30):
    wait = WebDriverWait(driver, timeout)
    try:
        wait.until(EC.invisibility_of_element_located((By.XPATH, "/html/body/div[2]")))
        print("web page loaded according to checking function")
        return True

    except TimeoutException:
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        driver.refresh()
        print("Timed out waiting for page to load")
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
    time.sleep(AfterClickWaitTime)
    
    print("waiting for page to load")
    if (wait_for_page_load(driver) != True):
        return "website timed out"
    
    try: 
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#form_goto_offer")))
        driver.refresh()
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        print("smart move offer found")
        return "unavailable"
    except TimeoutException:
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//h4[@class="widget-heading widget-heading--center" and text()="Give us a call to discover your options:"]')))
            print("Smart move suggestion screen")
            driver.delete_all_cookies()
            driver.execute_script("window.localStorage.clear();")
            driver.execute_script("window.sessionStorage.clear();")
            driver.refresh()
            return "unavailable"
        except TimeoutException:
            print("could not locate smart move identifier")
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-primary.text-white.text-underline-none.w-100")))
                print("found available identifier")
                ### SCRAPE SPEED
                
                driver.back()
                driver.delete_all_cookies()
                driver.execute_script("window.localStorage.clear();")
                driver.execute_script("window.sessionStorage.clear();")
                driver.refresh()
                return "available" 
            except:
                try:
                    wait.until(EC.presence_of_element_located((By.XPATH, '//h1[@class="heavy--5 text-gray-medium" and text()="Error!"]')))
                    print("Error! identifier located")
                    ### SCRAPE SPEED
                    
                    driver.back()
                    driver.delete_all_cookies()
                    driver.execute_script("window.localStorage.clear();")
                    driver.execute_script("window.sessionStorage.clear();")
                    driver.refresh()
                    return "available"
                except:
                    print("could not find error identifier")
                    return search_address(address, zipCode, driver, wait, searchBar, zipCodeBar, searchButton, retries-1)


def process(data):
    driver = webdriver.Firefox(options=options)
    exception_occurred = False
    try:
        driver.get(website)
        ### NAVIGATE PAGE
        wait = WebDriverWait(driver, 10)
        
        ### SEARCH AND SCRAPE
        for row in data[1:(chunk+1)]:
            address = ", ".join(row[2:5])
            zipCode = row[5]
            
            searchBar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#update-address-comp-input-")))
            zipCodeBar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#update-zip-comp-input-")))
            searchButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#btn-update-address-comp-")))
                
            availability = search_address(address, zipCode, driver, wait, searchBar, zipCodeBar, searchButton, 5)
            row[7] = availability
            time.sleep(1.5)
            
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
    
    
# smart move identifiers
'''wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#form_goto_offer")) or
            EC.presence_of_element_located((By.CSS_SELECTOR, "#form_see_offers")) or
            EC.presence_of_element_located((By.CSS_SELECTOR, "#smartmove-placeholder-")) or
            EC.presence_of_element_located((By.CSS_SELECTOR, ".col-lg-7")) or
            EC.presence_of_element_located((By.ID, "internet-service-areas")))'''
    
"""    # Multithreading Uniti scraper
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

chunk = 10
in_file = "test.csv"
out_file = "output.csv"
website = "https://www.sparklight.com/internet"

### SET UP BROWSER PREFERENCES
options = Options()
user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
options.set_preference("general.useragent.override", user_agent) # Set user agent to bypass website blocking
options.set_preference("dom.webdriver.enabled", False) # Disable webdriver mode to bypass website blocking

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
    
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#form_goto_offer")) or
                   EC.presence_of_element_located((By.CSS_SELECTOR, "#form_see_offers")) or
                   EC.presence_of_element_located((By.CSS_SELECTOR, "h4.widget-heading.widget-heading--center")))
        print("smart move suggestion screen")
        time.sleep(4)
        driver.refresh()
        return "unavailable"
    except TimeoutException:
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#form_see_offers")))
            print("smart move can't find available ISP")
            time.sleep(4)
            driver.refresh()
            return "unavailable 2" # Smart move can't locate a single provider Do I need to differentiate?
        except TimeoutException: # 30 second already passed no need to wait more
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-primary.text-white.text-underline-none.w-100")))
                ### SCRAPE SPEED
                return "available" 
            except:
                driver.save_screenshot('unexpected_page.png')
                driver.quit()


def process(data):
    driver = webdriver.Firefox(options=options)
    exception_occurred = False
    try:
        driver.get(website)
        ### NAVIGATE PAGE
        wait = WebDriverWait(driver, 15)
        
        ### SEARCH AND SCRAPE
        for row in data[1:(chunk+1)]:
            address = ", ".join(row[2:5])
            zipCode = row[5]
            
            searchBar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#update-address-comp-input-")))
            zipCodeBar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#update-zip-comp-input-")))
            searchButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#btn-update-address-comp-")))
                
            availability = search_address(address, zipCode, driver, wait, searchBar, zipCodeBar, searchButton, 5)
            row[7] = availability
            time.sleep(1.5)
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
    writer.writerows(flattened_processed_data)"""