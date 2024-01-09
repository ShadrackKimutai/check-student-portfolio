import time
import tkinter as tk
import os 
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_unique_subpages(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        subpages = {urljoin(url, link['href']) for link in links}
        return list(subpages)
    except Exception as e:
        return [f"Error: {str(e)}"]
    
def getPageScreenshot(url,dirName):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--start-maximized")
        browser = webdriver.Chrome(options=options)
        browser.get(url)
        s=browser.current_url
        s=s.replace('https://sites.google.com/view/'+dirName,'')
        s=s.replace('/','')
        
        height = browser.execute_script('return document.documentElement.scrollHeight')
        width  = browser.execute_script('return document.documentElement.scrollWidth')
        browser.set_window_size(width, height)
        time.sleep(2)
        browser.save_screenshot(dirName+"/"+s+".png")
        browser.quit()
    except Exception as e:
        print(f"Error Getting Screenshot:{str(e)}")
    return
def getDirectoryName(s):
        s=s.replace('https://sites.google.com/view','')
        return s.replace('/','')
def fetch_unique_subpages():
    url = entry.get()
    dirName=getDirectoryName(url)
    if not os.path.exists(dirName):
            os.makedirs(dirName)
    unique_subpages = get_unique_subpages(url)

    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)

    for subpage in unique_subpages:
        result_text.insert(tk.END, subpage + '\n')

    result_text.config(state=tk.DISABLED)

    for subpage in unique_subpages:
        getPageScreenshot(subpage,dirName)

# Create the main window
root = tk.Tk()
root.title("Webpage Unique Subpages Extractor")

# Create and place widgets
label = ttk.Label(root, text="Enter URL:")
label.grid(row=0, column=0, padx=10, pady=10)

entry = ttk.Entry(root, width=40)
entry.grid(row=0, column=1, padx=10, pady=10)

fetch_button = ttk.Button(root, text="Fetch Unique Subpages", command=fetch_unique_subpages)
fetch_button.grid(row=1, column=0, columnspan=2, pady=10)

result_text = tk.Text(root, wrap=tk.WORD, height=10, width=60)
result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
result_text.config(state=tk.DISABLED)

# Run the Tkinter event loop
root.mainloop()

