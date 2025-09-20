import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

st.title("📉 Macro Relations")

df = pd.read_csv("econ/all.csv")

# Philips Curve
st.subheader("Philips Curve: Inflation vs Unemployment")
fig = px.scatter(
    df,
    x="Unemployment, total (% of total labor force)",
    y="Inflation, consumer prices (annual %)",
    text="Year",
    trendline="ols",
    labels={
        "Unemployment, total (% of total labor force)": "Unemployment (%)",
        "Inflation, consumer prices (annual %)": "Inflation (%)"
    },
    title="Philips Curve"
)
fig.update_traces(textposition="top center")
st.plotly_chart(fig, use_container_width=True)

# Correlation Heatmap
st.subheader("Correlation Heatmap of Key Economic Variables")
selected_cols = [
    "Inflation, consumer prices (annual %)",
    "GDP growth (annual %)",
    "Unemployment, total (% of total labor force)",
    "Total Debt stock",
    "Dollar Exchange Rate",
    "Copper US /Tonne",
    "Broad Money (M3)"
]

corr = df[selected_cols].corr().round(2)
heatmap = ff.create_annotated_heatmap(
    z=corr.values,
    x=list(corr.columns),
    y=list(corr.index),
    annotation_text=corr.values.astype(str),
    colorscale="RdBu",
    reversescale=True
)
st.plotly_chart(heatmap, use_container_width=True)
