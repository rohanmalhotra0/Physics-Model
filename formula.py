import pandas as pd
import numpy as np
import pickle


# Load the DataFrame from the Excel file
df = pd.read_excel("spy_daily_data.xlsx")

# Drop any NaNs just in case
df.dropna(subset=["close", "SMA50"], inplace=True)

# Implement the formula here
# Get the most recent (last) row
latest = df.iloc[-1]

# Initialize counter
numBuy = 0

# Compare close to SMA50
if latest["close"] < latest["SMA50"]:
    numBuy += 1

print("numBuy =", numBuy)





