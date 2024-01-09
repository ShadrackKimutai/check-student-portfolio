from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.keys import Keys
options = Options()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)
browser.get("https://sites.google.com/view/shadrackkimutai")
s=browser.current_url
s=s.replace('https://','')
s=s.replace('/','')

browser.save_screenshot(s+".png")
browser.close()
