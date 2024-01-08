from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
browser.get("https://www.google.com")
print(str.replace('https://',browser.current_url))
#browser.save_screenshot("link"+browser.current_url+".png")
browser.close()
