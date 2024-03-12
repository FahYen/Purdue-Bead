# Multithreading Uniti scraper
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
import csv
import concurrent.futures

### SET UP BROWSER PREFERENCES
options = Options()
user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
options.set_preference("general.useragent.override", user_agent) # Set user agent to bypass website blocking
options.set_preference("dom.webdriver.enabled", False) # Disable webdriver mode to bypass website blocking

### DEFINE SINGLE THREAD OPERATION
def process(data):
    driver = webdriver.Firefox(options=options)
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
    for row in data[1:(2000+1)]:
        address = ", ".join(row[2:6])
        searchBar.clear()
        searchBar.send_keys(address) # Send address
        # Find the obscuring element
        loadingIndicator = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "jimu_dijit_LoadingIndicator_1")))
        # Wait until the obscuring element is no longer visible
        wait.until(EC.invisibility_of_element(loadingIndicator))
        
        time.sleep(random.randint(7, 11) / random.randint(4, 10)) # Sleep for a random amount of time to avoid bot detection
        searchButton.click() # Click on searh button
        time.sleep(random.randint(8, 12) / random.randint(5, 10))
        try:
            # Try to find the element that indicates the address is not served
            WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CLASS_NAME, "esriCTNoFeatureFound")))
            availability = "unavailable"
        except TimeoutException:
            # If the element is not found
            try: # Find unable to fetch results from layers pop-up
                ok_button = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.jimu-btn:nth-child(1)")))
                ok_button.click()
                availability = "error"
            except TimeoutException:
                availability = "available"
                
        row[7] = availability
        offset = random.randint(-20, 20) # Scrol down to range with random offset
        driver.execute_script(f"window.scrollBy(0, {offset});")
        time.sleep(random.randint(5, 15) / random.randint(4, 7))
    return data

### INITIALIZE MULTITHREADING
with open("underserved1.csv", "r") as file:
    reader = csv.reader(file)
    data = list(reader)
chunks = [data[i:i + 500] for i in range(0, len(data), 500)]
with concurrent.futures.ThreadPoolExecutor() as executor:
    processed_data = list(executor.map(process, chunks))
flattened_processed_data = [item for sublist in processed_data for item in sublist]
with open("output2.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerows(flattened_processed_data)

#Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0
# '.jimu-btn.jimu-popup-action-btn.jimu-float-trailing.jimu-trailing-margin1')
# div.jimu-btn:nth-child(1)
# <div class="jimu-btn jimu-state-disabled jimu-float-trailing jimu-trailing-margin1  " title="OK" tabindex="0" role="button" aria-disabled="true" style="display: none;">OK</div>

# Ok button: div.jimu-btn:nth-child(1)