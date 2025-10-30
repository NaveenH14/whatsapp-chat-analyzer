import streamlit as st
import pandas as pd
import re
from datetime import datetime

st.title("📊 WhatsApp Chat Analyzer")

# 🔹 Let user upload the txt file
uploaded_file = st.file_uploader("Upload your WhatsApp chat (.txt)", type=["txt"])

if uploaded_file is not None:
    lines = uploaded_file.getvalue().decode("utf-8").splitlines()

    pattern = re.compile(r"^(\d{2}-\d{2}-\d{4}) (\d{2}:\d{2}:\d{2}) - (.*?): (.*)")
    data = []
    for line in lines:
        match = pattern.match(line.strip())
        if match:
            date, time, sender, message = match.groups()
            data.append([date, time, sender, message])

    df = pd.DataFrame(data, columns=["Date", "Time", "Sender", "Message"])
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce")
    df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce").dt.time
    df["DateTime"] = pd.to_datetime(df["Date"].astype(str) + " " + df["Time"].astype(str), errors="coerce")

    st.success("✅ File loaded successfully!")
    st.write(f"📅 Date range: {df['Date'].min().date()} → {df['Date'].max().date()}")
    st.write(f"💬 Total messages: {len(df)}")
    st.dataframe(df.head())
else:
    st.info("👆 Upload a WhatsApp chat text file to begin analysis.")
