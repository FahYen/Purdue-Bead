from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
import csv

### SET UP BROWSER
options = Options()
user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
options.set_preference("general.useragent.override", user_agent) # Set user agent to bypass website blocking
options.set_preference("dom.webdriver.enabled", False) # Disable webdriver mode to bypass website blocking
driver = webdriver.Firefox(options=options)
driver.get("https://uniti.com/network-map/")
time.sleep(2.5)

### NAVIGATE PAGE
wait = WebDriverWait(driver, 15) # Maximum wait time
iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".divi-overlay-iframe-wrap > iframe:nth-child(1)")))
driver.switch_to.frame(iframe) # Switch to the ArcGIS frame
offset = random.randint(400, 600) # Scrol down to range with random offset
driver.execute_script(f"window.scrollBy(0, {offset});")
searchBar = wait.until(EC.presence_of_element_located((By.ID, "esri_dijit_Search_0_input"))) # Find element
searchButton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.searchBtn:nth-child(2)"))) # Find element

### SEARCH
searchBar.clear()
searchBar.send_keys("16476 N 300 W,COVINGTON,IN,47932") # Send address
time.sleep(random.randint(7, 11) / random.randint(2, 4)) # Sleep for a random amount of time to avoid bot detection
searchButton.click() # Click on searh button
time.sleep(random.randint(8, 12) / random.randint(3, 5))

# Get the availability data and add it to the row
try:
    # Try to find the element that indicates the address is not served
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "esriCTNoFeatureFound")))
    availability = "not available"
except TimeoutException:
    # If the element is not found, the address is served
    availability = "available"

print(availability)