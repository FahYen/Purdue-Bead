from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

ISP = ["https://www.xfinity.com/national/"]
addresses = ["1132 Pennsylvania St Gary", "695 E County Road 50 N Winamac", "653 Arthur Rd Springville"]

chrome_options = Options()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')

driver = webdriver.Chrome(options=chrome_options)
driver.get(ISP[0])

wait = WebDriverWait(driver, 30)  # Wait up to 30 seconds

input_element = wait.until(EC.element_to_be_clickable((By.ID, "prism-input-text-d572cc97-c5b5-47d0-a324-2b54303b8731")))
input_element.send_keys(addresses[0])

print("Page Title:", driver.title)
driver.quit()
