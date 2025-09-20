import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Growth & Debt")

df = pd.read_csv("econ/all.csv")

# GDP Growth
st.subheader("GDP Growth (%)")
fig_growth = px.line(df, x="Year", y="GDP growth (annual %)", markers=True,
                     title="GDP Growth Rate")
st.plotly_chart(fig_growth, use_container_width=True)

# GDP Level
st.subheader("GDP (Current US$)")
fig_gdp = px.line(df, x="Year", y="GDP (current US$)", markers=True,
                  title="GDP (Current US$)")
st.plotly_chart(fig_gdp, use_container_width=True)

# Debt stock
st.subheader("Debt Stock")
fig_debt = px.line(df, x="Year", y="Total Debt stock", markers=True,
                   title="Total Debt Stock")
st.plotly_chart(fig_debt, use_container_width=True)

# Lending rates
st.subheader("Lending & Interbank Rates")
fig_rates = px.line(
    df,
    x="Year",
    y=["Weighted Lending Base rate", "Average Lending Rate", "Weighted Interbank Rate"],
    markers=True,
    title="Lending & Interbank Rates"
)
st.plotly_chart(fig_rates, use_container_width=True)
