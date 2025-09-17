import streamlit as st
import pandas as pd
from utils.helpers import load_budget_data

st.title("🌍 Comparative Analysis")

data = load_budget_data()

if data is not None:
    st.subheader("Multi-Year Trends")

    # Line charts for macroeconomic trends
    st.line_chart(data.set_index("Year")[["GDP_Growth", "Inflation"]])

    st.subheader("Sector Budget Shares Over Time")
    st.area_chart(data.set_index("Year")[["Health", "Education", "Infrastructure", "Agriculture", "Social_Protection"]])

    st.markdown("This helps visualize long-term shifts in Zambia’s budget priorities.")
else:
    st.warning("Upload or fill `data/budget_data.csv` to see results.")
