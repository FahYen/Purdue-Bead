from selenium import webdriver # To initialize the browser
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By # To locate elements by ID
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # To wait until required elements are loaded

ISP_address = ["https://www.xfinity.com/national/"]
home_address = ["1132 Pennsylvania St Gary", "695 E County Road 50 N Winamac", "653 Arthur Rd Springville"]

chrome_options = Options()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')

driver = webdriver.Chrome(options=chrome_options)
driver.get(ISP_address[0])
# Success
# id is different everytime. Has to find button through some other way

wait = WebDriverWait(driver, 40)
input_element = wait.until(EC.element_to_be_clickable((By.NAME, "input text contained body1 sc-prism-input-text")))
input_element.send_keys(home_address[0])

print("Page Title:", driver.title)
driver.quit()

# Address input element
# <input class="input text contained body1 sc-prism-input-text" id="prism-input-text-d572cc97-c5b5-47d0-a324-2b54303b8731" autocapitalize="off" autocomplete="street-address" autocorrect="off" inputmode="text" name="localizationAddressField" placeholder="123 Main St, Apt J, Pleasantville, MA 01040" role="combobox" type="text" aria-invalid="false" aria-required="false" aria-controls="localization-suggestions" aria-expanded="false" aria-autocomplete="list">
# <input class="input text contained body1 sc-prism-input-text" id="prism-input-text-81d86e6b-1a49-4800-8351-c22139f98a12" autocapitalize="off" autocomplete="street-address" autocorrect="off" inputmode="text" name="localizationAddressField" placeholder="123 Main St, Apt J, Pleasantville, MA 01040" role="combobox" type="text" aria-invalid="false" aria-required="false" aria-controls="localization-suggestions" aria-expanded="true" aria-autocomplete="list">
# <input class="input text contained body1 sc-prism-input-text" id="prism-input-text-a489f424-1c06-4251-952f-f97ac9addded" autocapitalize="off" autocomplete="street-address" autocorrect="off" inputmode="text" name="localizationAddressField" placeholder="123 Main St, Apt J, Pleasantville, MA 01040" role="combobox" type="text" aria-invalid="false" aria-required="false" aria-controls="localization-suggestions" aria-expanded="true" aria-autocomplete="list">

# //*[@id="prism-input-text-db1e7b95-893d-460c-a48b-c15992c02c8f"]
# //*[@id="prism-input-text-c880f947-bf1c-46da-b7b3-79fb196085d3"]