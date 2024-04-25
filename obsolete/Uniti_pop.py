from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time
import random
import csv

def search_address(address, driver, wait, searchBar, searchButton, data, i):
    searchBar.clear()
    searchBar.send_keys(address) # Send address
    time.sleep(random.randint(7, 11) / random.randint(2, 4)) # Sleep for a random amount of time to avoid bot detection
    # Find the obscuring element
    loadingIndicator = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "jimu_dijit_LoadingIndicator_1")))
    # Wait until the obscuring element is no longer visible
    wait.until(EC.invisibility_of_element(loadingIndicator))
    time.sleep(1.5)
    try:
        searchButton.click() # Click on searh button
    except ElementClickInterceptedException:
        with open("outputIncomplete.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data[:i+1])
 
    time.sleep(random.randint(8, 12) / random.randint(3, 5))
    try:
        # Try to find the element that indicates the address is not served
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "esriCTNoFeatureFound")))
        availability = "unavailable"
    except TimeoutException:
        try: # Find address is served indicator
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Congratulations! This address is close to our fiber network and can be served by Uniti.')]")))
            availability = "available"
        except TimeoutException:
            try: # Find unable to fetch results from layers pop-up
                ok_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[text()='OK']")))
                time.sleep(10)
                ok_button.click()
                return search_address(address)
            except TimeoutException:
                availability = "available"
    return availability

def main(website, input, output):
    ### SET UP BROWSER
    options = Options()
    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
    options.set_preference("general.useragent.override", user_agent) # Set user agent to bypass website blocking
    options.set_preference("dom.webdriver.enabled", False) # Disable webdriver mode to bypass website blocking
    driver = webdriver.Firefox(options=options)
    
    driver.get(website)
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
    with open(input, "r") as file:
        reader = csv.reader(file)
        data = list(reader)

    for i, row in enumerate(data[1:(2000+1)]):
        address = ", ".join(row[2:6])
        availability = search_address(address, driver, wait, searchBar, searchButton, data, i)
        row[7] = availability
        offset = random.randint(-20, 20) # Scrol down to range with random offset
        driver.execute_script(f"window.scrollBy(0, {offset});")
        time.sleep(random.randint(5, 15) / random.randint(4, 7))

    with open(output, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
if __name__ == "__main__":
    website = "https://uniti.com/network-map/"
    input = "underserved1.csv"
    output = "output.csv"
    main(website, input, output)
