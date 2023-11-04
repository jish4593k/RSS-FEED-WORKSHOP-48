import feedparser
import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

# Function to fetch RSS feed data
def fetch_rss_data(feed_url):
    try:
        feed = feedparser.parse(feed_url)
        data = []
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            data.append((title, link))
        return data
    except Exception as e:
        return None

# Function to display RSS feed data in a Pandas DataFrame
def display_rss_data(data):
    if data:
        df = pd.DataFrame(data, columns=["Title", "Link"])
        return df
    else:
        return None

# Function to plot the number of articles per source
def plot_article_counts(df):
    if df is not None:
        source_counts = df["Link"].apply(lambda x: x.split("/")[2]).value_counts()
        source_counts.plot(kind="bar")
        plt.title("Number of Articles per Source")
        plt.xlabel("Source")
        plt.ylabel("Count")
        plt.show()

# Function to update the GUI with RSS feed data and plot
def update_gui(feed_url):
    data = fetch_rss_data(feed_url)
    if data:
        df = display_rss_data(data)
        output_text.delete("1.0", "end")
        output_text.insert("1.0", df.to_string(index=False))
        plot_article_counts(df)
        status_label.config(text=f"Loaded RSS feed from {feed_url}")
    else:
        status_label.config(text="Invalid RSS feed URL")

# Function to clear the output
def clear_output():
    output_text.delete("1.0", "end")
    status_label.config(text="Output cleared")

# Function to save data to a CSV file
def save_to_csv():
    data = output_text.get("1.0", "end")
    if data.strip():
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            with open(filename, "w") as file:
                file.write(data)
            status_label.config(text=f"Data saved to {filename}")
    else:
        status_label.config(text="No data to save")

# Function to open the CSV file in the default CSV viewer
def open_csv_viewer():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filename:
        import os
        os.system(f"start {filename}")

# Create a simple Tkinter GUI
root = tk.Tk()
root.title("RSS Feed Viewer")
root.minsize(600, 400)

frame = ttk.Frame(root)
frame.pack(pady=10)

url_label = ttk.Label(frame, text="RSS Feed URL:")
url_label.grid(row=0, column=0)

url_entry = ttk.Entry(frame, width=40)
url_entry.grid(row=0, column=1)

fetch_button = ttk.Button(frame, text="Fetch RSS Data", command=lambda: update_gui(url_entry.get())
                         ,cursor="hand2"
                         ,tooltip="Fetch RSS data from the given URL")
fetch_button.grid(row=0, column=2)

clear_button = ttk.Button(frame, text="Clear Output", command=clear_output
                         ,cursor="hand2"
                         ,tooltip="Clear the displayed RSS data")
clear_button.grid(row=0, column=3)

save_button = ttk.Button(frame, text="Save to CSV", command=save_to_csv
                        ,cursor="hand2"
                        ,tooltip="Save the displayed data to a CSV file")
save_button.grid(row=0, column=4)

open_csv_button = ttk.Button(frame, text="Open CSV", command=open_csv_viewer
                            ,cursor="hand2"
                            ,tooltip="Open the saved CSV file in the default CSV viewer")
open_csv_button.grid(row=0, column=5)

output_text = tk.Text(frame, height=15, width=60)
output_text.grid(row=1, column=0, columnspan=6)

status_label = ttk.Label(frame, text="Welcome to RSS Feed Viewer")
status_label.grid(row=2, column=0, columnspan=6)

scrollbar = ttk.Scrollbar(frame, command=output_text.yview)
scrollbar.grid(row=1, column=6, sticky="nsew")
output_text['yscrollcommand'] = scrollbar.set

root.mainloop()
