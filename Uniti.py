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
with open("underserved7K.csv", "r") as file:
    reader = csv.reader(file)
    data = list(reader)
    
for row in data[1:(2000+1)]:
    address = ", ".join(row[2:6])
    searchBar.clear()
    searchBar.send_keys(address) # Send address
    # Find the obscuring element
    loadingIndicator = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "jimu_dijit_LoadingIndicator_1")))
    # Wait until the obscuring element is no longer visible
    wait.until(EC.invisibility_of_element(loadingIndicator))
    time.sleep(1.5)
    searchButton.click() # Click on searh button
    time.sleep(1.5)
    try:
        # Try to find the element that indicates the address is not served
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "esriCTNoFeatureFound")))
        availability = "unavailable"
    except TimeoutException:
        try: # Find address is served indicator
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Congratulations! This address is close to our fiber network and can be served by Uniti.')]")))
            availability = "available"
        except TimeoutException:
            try: # Find unable to fetch results from layers pop-up
                ok_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[text()='OK']")))
                time.sleep(10)
                ok_button.click()
                availability = "error"
            except TimeoutException:
                availability = "available"
    row[7] = availability
    offset = random.randint(-20, 20) # Scrol down to range with random offset
    driver.execute_script(f"window.scrollBy(0, {offset});")
    time.sleep(1.5)


with open("output2K.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data[:2000 + 1])
    



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

# address found
# <div class="dijitContentPane esriCTFeatureInfo" id="dijit_layout_ContentPane_0" widgetid="dijit_layout_ContentPane_0" tabindex="0" role="document"><div class="dijitContentPane" id="dijit_layout_ContentPane_57" style="padding: 0px;" widgetid="dijit_layout_ContentPane_57"><div class="esriCTDistanceToLocation">Approximate Distance: 304.19 ft</div></div><div class="dijitContentPane esriCTPopupInfo" id="dijit_layout_ContentPane_58" widgetid="dijit_layout_ContentPane_58"><div class="esriViewPopup" id="esri_dijit__PopupRenderer_28" widgetid="esri_dijit__PopupRenderer_28"><div class="statusSection hidden" dojoattachpoint="_status"></div><div class="mainSection"><div class="header" dojoattachpoint="_title">Address Validator</div><div class="hzLine"></div><div dojoattachpoint="_description"><span style=""><font face="Arial" size="3">Congratulations! This address is close to our fiber network and can be served by Uniti. Click&nbsp;</font></span><a href="https://connect.uniti.com/acton/media/45225/uniti-fiber-on-net-location" target="_blank"><font size="3">here</font></a><span style=""><font face="Arial" size="3">&nbsp;to connect with a Uniti expert today!</font></span></div><div class="break"></div></div><div class="attachmentsSection"></div><div class="mediaSection hidden esriCTHidden"><div class="header" dojoattachpoint="_mediaTitle"></div><div class="hzLine"></div><div class="caption" dojoattachpoint="_mediaCaption"></div><div class="gallery" dojoattachpoint="_gallery"><div class="mediaHandle prev" dojoattachpoint="_prevMedia" dojoattachevent="onclick: _goToPrevMedia" title="Previous media"></div><div class="mediaHandle next" dojoattachpoint="_nextMedia" dojoattachevent="onclick: _goToNextMedia" title="Next media"></div><ul class="summary"><li class="image mediaCount hidden" dojoattachpoint="_imageCount">0</li><li class="image mediaIcon hidden"></li><li class="chart mediaCount hidden" dojoattachpoint="_chartCount">0</li><li class="chart mediaIcon hidden"></li></ul><div class="frame" dojoattachpoint="_mediaFrame"></div></div></div><div class="editSummarySection hidden" dojoattachpoint="_editSummarySection"><div class="break"></div><div class="break hidden" dojoattachpoint="_mediaBreak"></div><div class="editSummary" dojoattachpoint="_editSummary"></div></div></div></div></div>
# Ok button appeared when: 1570 E DENTON RD, LEAVENWORTH, IN, 47137