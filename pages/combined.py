# combined.py

import pandas as pd
import plotly.express as px
import streamlit as st

# ----------------------
# PAGE CONFIG
# ----------------------
st.set_page_config(page_title="Revenue vs Expenditure Analysis", layout="wide")
st.title("📊 Combined Revenue & Expenditure Analysis (2007–2025)")

# ----------------------
# LOAD DATA
# ----------------------
@st.cache_data
def load_revenue():
    df = pd.read_csv("csv_output/REVENUE.csv", encoding="latin-1")
    df.columns = df.columns.str.strip().str.replace('"', '').str.replace("\n", " ")
    df["Year"] = df["Year"].astype(int)
    for col in df.columns:
        if col != "Year":
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "").str.replace(" ", ""), errors="coerce")
    return df

@st.cache_data
def load_expenditure():
    df = pd.read_csv("csv_output/EXPENDITURE.csv", encoding="latin-1")
    df.columns = df.columns.str.strip().str.replace('"', '').str.replace("\n", " ")
    df["Year"] = df["Year"].astype(int)
    for col in df.columns:
        if col != "Year":
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "").str.replace(" ", ""), errors="coerce")
    return df

revenue_df = load_revenue()
expenditure_df = load_expenditure()

# ----------------------
# MERGE DATA
# ----------------------
df = pd.merge(
    revenue_df[["Year", "Domestic Revenue", "Tax Revenue", "Non-Tax Revenue", "Grants", "DOMESTIC REVENUE, GRANTS AND FINANCING", 
                "Domestic Financing", "Foreign Financing"]],
    expenditure_df[["Year", "Total_Expenditure", "General Public Services", "Defence", "Public Order and Safety",
                    "Economic Affairs", "Environmental Protection", "Housing and Community Amenities",
                    "Health", "Recreation, Culture and Religion", "Education", "Social Protection"]],
    on="Year",
    how="inner"
)

# Rename total revenue for clarity
df = df.rename(columns={"DOMESTIC REVENUE, GRANTS AND FINANCING": "Total Revenue"})

# ----------------------
# DERIVED METRICS
# ----------------------
# Fiscal deficit based on domestic revenue
df["Fiscal Deficit (Absolute)"] = df["Total_Expenditure"] - df["Domestic Revenue"]
df["Fiscal Deficit (% of Domestic Revenue)"] = df["Fiscal Deficit (Absolute)"] / df["Domestic Revenue"] * 100

# Expenditure/Revenue ratio
df["Expenditure/Revenue (%)"] = df["Total_Expenditure"] / df["Domestic Revenue"] * 100

# Growth rates
df["Revenue Growth (%)"] = df["Domestic Revenue"].pct_change() * 100
df["Expenditure Growth (%)"] = df["Total_Expenditure"].pct_change() * 100

# ----------------------
# ADMINISTRATION
# ----------------------
def get_admin(year):
    if year <= 2011:
        return "MMD (2007–2011)"
    elif year <= 2021:
        return "PF (2011–2021)"
    else:
        return "UPND (2021–Present)"

df["Administration"] = df["Year"].apply(get_admin)

# ----------------------
# VISUALIZATIONS
# ----------------------
st.subheader("Revenue vs Expenditure Over Time")
fig = px.line(
    df,
    x="Year",
    y=["Domestic Revenue", "Total Revenue", "Total_Expenditure"],
    markers=True,
    color_discrete_map={
        "Domestic Revenue": "green",
        "Total Revenue": "lightgreen",
        "Total_Expenditure": "red"
    },
    title="Revenue vs Expenditure"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Fiscal Deficit Trends")
fig = px.line(
    df,
    x="Year",
    y=["Fiscal Deficit (Absolute)", "Fiscal Deficit (% of Domestic Revenue)"],
    markers=True,
    title="Fiscal Deficit Over Time"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Revenue and Expenditure by Administration")
fig = px.bar(
    df,
    x="Year",
    y=["Domestic Revenue", "Total_Expenditure"],
    color="Administration",
    barmode="group",
    title="Revenue vs Expenditure by Government Administration"
)
st.plotly_chart(fig, use_container_width=True)

# ----------------------
# STACKED COMPOSITION CHARTS
# ----------------------
st.subheader("Revenue Composition Over Time (Domestic Revenue + Grants)")
revenue_components = ["Domestic Revenue", "Grants"]
fig = px.bar(
    df,
    x="Year",
    y=revenue_components,
    title="Revenue Composition (Stacked)",
    labels={"value": "Amount (ZMW)", "variable": "Revenue Source"}
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Expenditure Composition Over Time")
expenditure_sectors = [
    "General Public Services", "Defence", "Public Order and Safety", "Economic Affairs",
    "Environmental Protection", "Housing and Community Amenities", "Health",
    "Recreation, Culture and Religion", "Education", "Social Protection"
]
fig = px.bar(
    df,
    x="Year",
    y=expenditure_sectors,
    title="Expenditure Composition by Sector (Stacked)",
    labels={"value": "Amount (ZMW)", "variable": "Sector"}
)
st.plotly_chart(fig, use_container_width=True)

# ----------------------
# DEFICIT FUNDING SOURCES
# ----------------------
st.subheader("Fiscal Deficit Funding Sources")
# Ensure no negative funding values
df["Grants_Funding"] = df["Grants"].clip(lower=0)
df["Domestic_Borrowing"] = df["Domestic Financing"].clip(lower=0)
df["Foreign_Borrowing"] = df["Foreign Financing"].clip(lower=0)

funding_cols = ["Grants_Funding", "Domestic_Borrowing", "Foreign_Borrowing"]
fig = px.bar(
    df,
    x="Year",
    y=funding_cols,
    title="How Fiscal Deficit is Financed (Stacked)",
    labels={"value": "Amount (ZMW)", "variable": "Funding Source"}
)
st.plotly_chart(fig, use_container_width=True)

# ----------------------
# QUICK INSIGHTS
# ----------------------
st.subheader("📌 Quick Insights")
latest_year = df["Year"].max()
latest_data = df.loc[df["Year"] == latest_year].iloc[0]

st.write(f"- Latest Year: **{latest_year}**")
st.write(f"- Domestic Revenue: **{latest_data['Domestic Revenue']:,.0f} ZMW**")
st.write(f"- Total Revenue (with Grants): **{latest_data['Total Revenue']:,.0f} ZMW**")
st.write(f"- Total Expenditure: **{latest_data['Total_Expenditure']:,.0f} ZMW**")
st.write(f"- Fiscal Deficit (Absolute): **{latest_data['Fiscal Deficit (Absolute)']:,.0f} ZMW**")
st.write(f"- Fiscal Deficit (% of Domestic Revenue): **{latest_data['Fiscal Deficit (% of Domestic Revenue)']:.2f}%**")

# ----------------------
# GROWTH RATES
# ----------------------
st.subheader("Revenue vs Expenditure Growth Rates")
fig = px.line(
    df,
    x="Year",
    y=["Revenue Growth (%)", "Expenditure Growth (%)"],
    markers=True,
    title="Growth Rate of Domestic Revenue vs Expenditure"
)
st.plotly_chart(fig, use_container_width=True)


