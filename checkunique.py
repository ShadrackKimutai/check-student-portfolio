import csv
import time
import tkinter as tk
import os 
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#folder processor
def createCSV():
    directory=entry.get()
    #Opens all folders in a directory, reads the contents of the first file
    #in each folder, and writes those contents to a single CSV file.
    #"""
    print(directory)
    with open('eportfolios.csv', 'w', newline='') as csvfile: #create eportfolios csv file for writing
        csv_writer = csv.writer(csvfile)

        for root, _, files in os.walk(directory):
            if files:  # Check if there are files in the folder
                first_file = files[0]  # Get the first file
                with open(os.path.join(root, first_file), 'r') as f:
                    contents = f.read()
                    csv_writer.writerow([contents])

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
        s=s.replace('https://sites.google.com/view/'+dirName.replace('.snapshot',''),'')
        s=s.replace('/','')

       # print('filename is '+s+' dirname is '+dirName)
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
        s=s.replace('https://sites.google.com/kttc.ac.ke','')

        return s.replace('/','')

def getBulkAddresses():
    filePath=txtcleancsv.get()
    with open(filePath, 'r') as file:
        urlList = csv.reader(file)
        for url in urlList:
            print(url[0])
            fetchUniqueSubPages(url[0])

def fetchUniqueSubPages(url):
    dirName=getDirectoryName(url)+'.snapshot'
    if not os.path.exists(dirName):
        os.makedirs(dirName)
    unique_subpages = get_unique_subpages(url)

    for subpage in unique_subpages:
        getPageScreenshot(subpage,dirName)

# Create the main window
root = tk.Tk()
root.title("Bulk Portfolio Snapshot process")

# Create and place widgets
label = ttk.Label(root, text="Select Path to folder downloaded from LMS")
label.grid(row=0, column=0, padx=10, pady=10)

label = ttk.Label(root, text="Select Path to Cleaned CSV")
label.grid(row=2, column=0, padx=10, pady=10)

txtentry = ttk.Entry(root, width=40)
txtentry.grid(row=0, column=1, padx=10, pady=10)

txtcleancsv=ttk.Entry(root, width=40)
txtcleancsv.grid(row=2, column=1, padx=10, pady=10)

btncreateCSV= ttk.Button(root, text="Fetch Portfolios", command=createCSV)
btncreateCSV.grid(row=1, column=0, columnspan=2, pady=10)

btnFetchPortfolios= ttk.Button(root, text="Fetch Portfolios", command=getBulkAddresses)
btnFetchPortfolios.grid(row=3, column=0, columnspan=2, pady=10)

# Run the Tkinter event loop
root.mainloop()

