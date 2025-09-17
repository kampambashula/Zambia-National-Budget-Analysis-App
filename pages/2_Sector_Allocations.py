import streamlit as st
import pandas as pd
from utils.helpers import load_budget_data

st.title("🏥📚 Sector Allocations")

data = load_budget_data()

if data is not None:
    st.subheader("Budget Allocations by Sector (% of Total Budget)")
    st.dataframe(data[["Year", "Health", "Education", "Infrastructure", "Agriculture", "Social_Protection"]])
    st.bar_chart(data.set_index("Year")[["Health", "Education", "Infrastructure", "Agriculture", "Social_Protection"]])
else:
    st.warning("Upload or fill `data/budget_data.csv` to see results.")
