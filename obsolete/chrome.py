# import undetected_chromedriver as uc #slow
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

driver = webdriver.Chrome('/Users/lambert/Downloads/chromedriver_mac_arm64/chromedriver')
driver.get('https://www.xfinity.com/national/')
driver.save_screenshot('nowsecure.png')

# https://www.verizon.com/home/internet/