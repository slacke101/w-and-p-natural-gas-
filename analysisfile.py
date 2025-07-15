# Nick Mastroni & Rafael Castro                  #
#         Date: 7-14-25                          #
#   Github: nick-mastroni-1718 , slacke101       #
# Natural Gas Withdrawls and Production in Texas #

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

#API request
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

# counts = df["process"].value_counts().reset_index()
# counts.columns = ["process", "count"]

# plt.figure(figsize=(10, 6))
# sns.barplot(data=counts, x="process", y="count")

# plt.title("Count of Distinct Values in 'process'")
# plt.xlabel("process")
# plt.ylabel("Count")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

print(df.head(10))






