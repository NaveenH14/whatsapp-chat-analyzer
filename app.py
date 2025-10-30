import pandas as pd
import re
import streamlit as st
from datetime import datetime

# Path to your txt file
file_path = "WhatsApp_Chat_Clean_For_ML_StandardTime.txt"

# Read the txt file
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Parse lines into structured columns
pattern = re.compile(r"^(\d{2}-\d{2}-\d{4}) (\d{2}:\d{2}:\d{2}) - (.*?): (.*)")
data = []
for line in lines:
    match = pattern.match(line.strip())
    if match:
        date, time, sender, message = match.groups()
        data.append([date, time, sender, message])

df = pd.DataFrame(data, columns=["Date", "Time", "Sender", "Message"])

# Convert date/time columns properly
df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce")
df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce").dt.time

# Optional: combine into single datetime column if you need
df["DateTime"] = df["Date"].astype(str) + " " + df["Time"].astype(str)
df["DateTime"] = pd.to_datetime(df["DateTime"], errors="coerce")

# ✅ Now you can safely show date range
st.write(f"📅 Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")

# You can then proceed with your ML or visualization logic
st.dataframe(df.head())
