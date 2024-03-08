from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.set_preference("dom.webdriver.enabled", False) # Disable webdriver mode to bypass website blocking

driver = webdriver.Firefox(options=options)
driver.get("https://www.xfinity.com/national/")

wait = WebDriverWait(driver, 10) # Maximum wait time

# Type in address
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".input.text.contained.body1.sc-prism-input-text"))).send_keys("1132 Pennsylvania St Gary, IN")
time.sleep(2)

# Click on the first suggestion
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".suggestions-select__item > span:nth-child(1)"))).click()
time.sleep(2)

# Click on "Check Availability"
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".btn.sm.neutral.fill.dir-row.horizontal.default.standard.sc-prism-button.sc-prism-button-s"))).click()
time.sleep(10)
driver.quit()

# Try Stealth browser and puppeteer https://pptr.dev