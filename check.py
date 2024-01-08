import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_subpages(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        subpages = [urljoin(url, link['href']) for link in links]
        return subpages
    except Exception as e:
        return f"Error: {str(e)}"


def fetch_subpages():
    url = entry.get()
    subpages = get_subpages(url)

    if isinstance(subpages, list):
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        for subpage in subpages:
            result_text.insert(tk.END, subpage + '\n')
        result_text.config(state=tk.DISABLED)
    else:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, subpages)
        result_text.config(state=tk.DISABLED)


# Create the main window
root = tk.Tk()
root.title("Webpage Subpages Extractor")

# Create and place widgets
label = ttk.Label(root, text="Enter URL:")
label.grid(row=0, column=0, padx=10, pady=10)

entry = ttk.Entry(root, width=40)
entry.grid(row=0, column=1, padx=10, pady=10)

fetch_button = ttk.Button(root, text="Fetch Subpages", command=fetch_subpages)
fetch_button.grid(row=1, column=0, columnspan=2, pady=10)

result_text = tk.Text(root, wrap=tk.WORD, height=10, width=60)
result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
result_text.config(state=tk.DISABLED)

# Run the Tkinter event loop
root.mainloop()

