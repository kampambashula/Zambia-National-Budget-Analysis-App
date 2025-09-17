import streamlit as st
import pandas as pd
from utils.helpers import load_budget_data

st.title("📈 Macroeconomic Fundamentals")

data = load_budget_data()

if data is not None:
    st.subheader("GDP Growth and Fiscal Indicators")
    st.dataframe(data[["Year", "GDP_Growth", "Inflation", "Deficit", "Debt_to_GDP"]])
else:
    st.warning("Please upload or add data in the `data/budget_data.csv` file.")
