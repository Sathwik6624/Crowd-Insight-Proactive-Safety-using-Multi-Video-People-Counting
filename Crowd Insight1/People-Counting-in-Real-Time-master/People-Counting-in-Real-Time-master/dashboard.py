import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="People Counting Dashboard", layout="wide")

st.title("📊 Live Multi-Camera People Counting Dashboard")

# Placeholder for graphs
chart_placeholder = st.empty()

# Store data
data = {
    "Camera 1": [],
    "Camera 2": []
}

while True:
    try:
        # Read latest data file
        df = pd.read_csv("data.csv")

        # Plot
        chart_placeholder.line_chart(df)

        time.sleep(1)

    except:
        st.warning("Waiting for data...")
        time.sleep(1)