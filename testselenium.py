from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
browser.get("https://www.google.com")
s=browser.current_url
print(s.replace('https://',''))
print(s.replace('/',''))

#browser.save_screenshot("link"+browser.current_url+".png")
browser.close()
