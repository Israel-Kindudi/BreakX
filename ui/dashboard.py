import streamlit as st
import json
import time
import pandas as pd

st.set_page_config(layout="wide")

st.title("⚡ BreakX Live Dashboard")

placeholder = st.empty()

while True:
    try:
        with open("data/signals.json", "r") as f:
            data = json.load(f)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Symbol", data["symbol"])
        col2.metric("Jump Probability", round(data["jump_probability"], 4))
        col3.metric("Confidence", round(data["confidence"], 4))
        col4.metric("Ranking", round(data["ranking"], 2))

        if data["signal"]:
            st.success(f"Signal: {data['signal']['action']}")
        else:
            st.info("No Signal")

        time.sleep(0.5)

    except:
        st.warning("Waiting for data...")
        time.sleep(1)