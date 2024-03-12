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
offset = random.randint(700, 900) # Scrol down to range with random offset
driver.execute_script(f"window.scrollBy(0, {offset});")
searchBar = wait.until(EC.presence_of_element_located((By.ID, "esri_dijit_Search_0_input"))) # Find element
searchButton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.searchBtn:nth-child(2)"))) # Find element

### SCRAPE AND POPULATE CSV
with open("underserved.csv", "r") as file:
    reader = csv.reader(file)
    data = list(reader)
    
for row in data[1:(500+1)]:
    address = ", ".join(row[2:6])
    searchBar.clear()
    searchBar.send_keys(address) # Send address
    time.sleep(random.randint(7, 11) / random.randint(2, 4)) # Sleep for a random amount of time to avoid bot detection
    # Find the obscuring element
    loadingIndicator = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "jimu_dijit_LoadingIndicator_1")))
    # Wait until the obscuring element is no longer visible
    wait.until(EC.invisibility_of_element(loadingIndicator))
    searchButton.click() # Click on searh button
    time.sleep(random.randint(8, 12) / random.randint(3, 5))
    try:
        # Try to find the element that indicates the address is not served
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "esriCTNoFeatureFound")))
        availability = "unavailable"
    except TimeoutException:
        # If the element is not found, the address is served
        availability = "available"
    row[7] = availability
    offset = random.randint(-20, 20) # Scrol down to range with random offset
    driver.execute_script(f"window.scrollBy(0, {offset});")
    time.sleep(random.randint(5, 15) / random.randint(4, 7))

with open("output2.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

# Result of address[0]
# <div class="esriCTNoFeatureFound" aria-label="<p><font face=&quot;Arial&quot; size=&quot;4&quot;>This address is not currently served by our fiber network but we are always expanding! Click&amp;nbsp;</font><a href=&quot;https://connect.uniti.com/acton/media/45225/off-net-fiber-validation&quot; target=&quot;_blank&quot;><font size=&quot;4&quot;>here</font></a><font face=&quot;Arial&quot; size=&quot;4&quot;>&amp;nbsp;to connect with a Uniti expert so we can learn more about your business needs.</font></p>"><p><font face="Arial" size="4">This address is not currently served by our fiber network but we are always expanding! Click&nbsp;</font><a href="https://connect.uniti.com/acton/media/45225/off-net-fiber-validation" target="_blank"><font size="4">here</font></a><font face="Arial" size="4">&nbsp;to connect with a Uniti expert so we can learn more about your business needs.</font></p></div>

# Boston for testing

# Test if navigation run for one cycle
# If do work, 
# try to find all possible speed result
# Work on scraping data from website to file
# Truncate exel file. 
#   combine address with state name into one column
#   reseach about if save exel to a pandas data frame or read it line by line


# Address with Uniti available: 8349 Dix Rd, Indianapolis, IN, 46259, USA