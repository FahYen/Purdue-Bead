# Multithreading Uniti scraper
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

chunk = 100

### SET UP BROWSER PREFERENCES
options = Options()
user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
options.set_preference("general.useragent.override", user_agent) # Set user agent to bypass website blocking
options.set_preference("dom.webdriver.enabled", False) # Disable webdriver mode to bypass website blocking

### SINGLE ADDRESS SCRAPING FUNCTION
def search_address(address, driver, wait, searchBar, searchButton, retries):
    if retries == 0:
        print("Retries exhausted. Skipping address...")
        return "website error, skipping address"
    searchBar.clear()
    searchBar.send_keys(address) # Send address
    try:
        # Find the obscuring element
        loadingIndicator = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "jimu_dijit_LoadingIndicator_1")))
        # Wait until the obscuring element is no longer visible
        wait.until(EC.invisibility_of_element(loadingIndicator))
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.searchBtn:nth-child(2)"))) # ADDED AT 2 AM MIGHT BE BUGGY WORKEd out it but slow
        searchButton.click() # Click on searh button
    except TimeoutException: # ElementClickInterceptedException: #should be timeoutexception
        # Find the obscuring element
        # loadingIndicator = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "jimu_dijit_LoadingIndicator_1")))
        # Wait until the obscuring element is no longer visible
        # wait.until(EC.invisibility_of_element(loadingIndicator))
        # searchButton.click()
        time.sleep(random.randint(3, 8))
        return search_address(address, driver, wait, searchBar, searchButton, retries-1)
    except ElementClickInterceptedException:
        time.sleep(random.randint(3, 8))
        return search_address(address, driver, wait, searchBar, searchButton, retries-1)
    time.sleep(1.5)
    try:
        # Address is not served indicator
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "esriCTNoFeatureFound"))) # LOOK FOR BOTH AT THE SAME TIME
        availability = "unavailable"
    except TimeoutException:
        try: # Address is served indicator
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Congratulations! This address is close to our fiber network and can be served by Uniti.')]")))
            availability = "available"
        except TimeoutException:
            try: # Find unable to fetch results from layers pop-up
                ok_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[text()='OK']")))
                # should be only button in the iframe
                # there is two buttons, one of them is unclickable. work on finding the one that's clickable
                # ok_button = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH, "//div[@role='button']")))
                time.sleep(random.randint(3, 8))
                ok_button.click()
                time.sleep(random.randint(15, 20))
                print("Website timed out. Retrying...")
                return search_address(address, driver, wait, searchBar, searchButton, retries-1)
            except TimeoutException:
                print("Slow internet. Retrying...")
                time.sleep(random.randint(3, 8))
                return search_address(address, driver, wait, searchBar, searchButton, retries-1)
                
    return availability
    
### DEFINE SINGLE THREAD OPERATION
def process(data):
    driver = webdriver.Firefox(options=options)
    exception_occurred = False
    try:
        driver.get("https://uniti.com/network-map/")
        time.sleep(2.5)
        ### NAVIGATE PAGE
        wait = WebDriverWait(driver, 15) # Maximum wait time 
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".divi-overlay-iframe-wrap > iframe:nth-child(1)")))
        driver.switch_to.frame(iframe) # Switch to the ArcGIS frame
        offset = random.randint(700, 900) # Scrol down to range with random offset
        driver.execute_script(f"window.scrollBy(0, {offset});")
        searchBar = wait.until(EC.presence_of_element_located((By.ID, "esri_dijit_Search_0_input"))) # Find element
        searchButton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.searchBtn:nth-child(2)"))) # Find element

        ### SEARCH AND SCRAPE
        for row in data[1:(chunk+1)]:
            address = ", ".join(row[2:6])
            availability = search_address(address, driver, wait, searchBar, searchButton, 3)
            row[7] = availability
            offset = random.randint(-20, 20) # Scrol down to range with random offset
            driver.execute_script(f"window.scrollBy(0, {offset});")
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
with open("underserved500.csv", "r") as file:
    reader = csv.reader(file)
    data = list(reader)
chunks = [data[i:i + chunk] for i in range(0, len(data), chunk)]
with concurrent.futures.ThreadPoolExecutor() as executor:
    processed_data = list(executor.map(process, chunks))
flattened_processed_data = [item for sublist in processed_data for item in sublist]
with open("500TestOutput.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerows(flattened_processed_data)

#Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0
# '.jimu-btn.jimu-popup-action-btn.jimu-float-trailing.jimu-trailing-margin1')
# div.jimu-btn:nth-child(1)
# ok button:
# <div class="jimu-btn jimu-state-disabled jimu-float-trailing jimu-trailing-margin1  " title="OK" tabindex="0" role="button" aria-disabled="true" style="display: none;">OK</div>

# Ok button: div.jimu-btn:nth-child(1)

#jimu_dijit_Message_1 > div:nth-child(2) > div:nth-child(1)

# selenium.common.exceptions.ElementClickInterceptedException: Message: Element <div class="searchBtn searchSubmit"> is not clickable at point (326,223) because another element <div class="jimu-overlay"> obscures it

# Exception occurred: Message: Element <div class="searchBtn searchSubmit"> is not clickable at point (326,222) because another element <div class="jimu-overlay"> obscures it
# Do a single thread test that makes the webdriver take a screenshot and pause when the exception happens, to see what that jim-overlay is doing. Maybe it's a loading screen that's not being waited for.