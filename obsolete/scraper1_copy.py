from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

ISP = ["https://www.xfinity.com"]
addresses = ["1132 Pennsylvania St Gary", "695 E County Road 50 N Winamac", "653 Arthur Rd Springville"]
# my user agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36

chrome_options = Options()
# chrome_options.add_argument("--headless")
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')

driver = webdriver.Chrome(options=chrome_options)
driver.get(ISP[0])

wait = WebDriverWait(driver, 30)  # Wait up to 10 seconds
# Click and fill address to search bar
# <input class="input text contained body1 sc-prism-input-text" id="prism-input-text-6465d36f-542b-48a8-b999-61c035ce2d0e" autocapitalize="off" autocomplete="street-address" autocorrect="off" inputmode="text" name="localizationAddressField" placeholder="1234 Main St, Apt J, Pleasantville MA 01040" role="combobox" type="text" aria-invalid="false" aria-required="false" aria-controls="localization-suggestions" aria-expanded="false" aria-autocomplete="list">
search_bar = wait.until(EC.presence_of_element_located((By.ID,'prism-input-text-6465d36f-542b-48a8-b999-61c035ce2d0e')))
address_input = driver.find_element(By.ID, 'prism-input-text-6465d36f-542b-48a8-b999-61c035ce2d0e')
address_input.clear()  # Clear any pre-filled text
address_input.send_keys(addresses[0])


wait = WebDriverWait(driver, 3)  # Wait up to 10 seconds
# Confirm Address by clicking on the dropdown confirmation address
driver.find_element(By.CSS_SELECTOR, "[data-testid='localization-eccopy'] a").click()

wait = WebDriverWait(driver, 3)  # Wait up to 10 seconds
# Click on "Build your plan" button
driver.find_element(By.CSS_SELECTOR, "[data-testid='prism-button-46b8a964-abef-4076-8bb2-e3624d7d6de2'] a").click()

wait = WebDriverWait(driver, 3)  # Wait up to 10 seconds
# Click on "Add New Account" button
# <button type="submit" class="x-button--solid" data-testid="additional-account-button"><span>Add New Account</span></button>'''
driver.find_element(By.CSS_SELECTOR, "[data-testid='additional-account-button']").click()

wait = WebDriverWait(driver, 3)  # Wait up to 10 seconds
# Click on "Add Internet" button
# <div data-testid="Internet-lob-drawer-cta" class="text-button1 ml-auto text-theme1-base mr-2 sm:mr-4">Add<span class="sr-only">Internet</span></div>
driver.find_element(By.CSS_SELECTOR, "[data-testid='Internet-lob-drawer-cta']").click()

wait = WebDriverWait(driver, 3)  # Wait up to 10 seconds
# Scraping the page
print("Page Title:", driver.title)


driver.quit()

