#    Nick Mastroni & Rafael Castro               #
#             Date: 7-14-25                      #
#   Github: nick-mastroni-1718 , slacke101       #
# Natural Gas Withdrawls and Production in Texas #


# Imports #
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import ttkbootstrap as ttk 
from ttkbootstrap.constants import *
import requests
import numpy as np

API_key = 'nPOAdzrvpGe1Xu5vHJs7CAdUtRgmRZfpmMh1gfsc' # API Key - US Energy & Administration #Nicks API Key 

API_url = 'https://api.eia.gov/v2/natural-gas/prod/sum/data/?frequency=monthly&data[0]=value&facets[duoarea][]=STX&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000'

headers = {
    "X-Api-Key": API_key
}

# API request #
response = requests.get(API_url, headers=headers)
response.raise_for_status()
data = response.json()

#Transform to pandas df
results = data.get("response", {}).get("data", [])
df = pd.DataFrame(results)

#remove None values in "value" column
df.replace("None", np.nan, inplace=True)
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)

# Fields/Variables #

class MainWindow:
    def __init__(self):                            # initializes object 
        self.root = ttk.Window(themename='vapor')  # sets theme for UI window
        self.root.title("Natural Gas Withdrawals and Production in Texas") #  title
        self.root.geometry("800x600")                                      # geometry of UI window

        style = ttk.Style()
        style.configure("AccentLine.TFrame", background="black")

        self.mainUI()

    def mainUI(self):                                                       # mainUI method, includes labels, widgets, buttons and more! (in progress)
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(
            self.main_frame,
            text="Home",
            font=("Segoe UI", 32, "bold"),
            bootstyle="primary"
        ).pack(anchor="w", pady=(10, 5))

        ttk.Separator(self.main_frame, orient="horizontal").pack(fill="x", pady=(0, 15))

              
   # Bar Chart Graph Method #     
    def barchartGraph(self):
        counts = df["process"].value_counts().reset_index()
        counts.columns = ["process", "count"]

        plt.figure(figsize=(10, 6))
        sns.barplot(data=counts, x="process", y="count")

        plt.title("Count of Distinct Values in 'process'")
        plt.xlabel("process")
        plt.ylabel("Count")
        plt.xticks(rotation=45)  # Rotate labels if needed
        plt.tight_layout()
        plt.show()
        
      
# Runs the Application #
if __name__ == "__main__":
    app = MainWindow()
    app.root.mainloop()





