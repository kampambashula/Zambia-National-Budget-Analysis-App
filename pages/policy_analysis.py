# policy_analysis.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ----------------------
# PAGE CONFIG
# ----------------------
st.set_page_config(page_title="Policy Analysis", layout="wide")
st.title("📊 Policy & Budget Constraint Analysis (2007–2025)")

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

rev_df = load_revenue()
exp_df = load_expenditure()

# ----------------------
# MERGE DATA
# ----------------------
df = pd.merge(
    rev_df[["Year", "Domestic Revenue", "Grants", "Domestic Financing", "Foreign Financing"]],
    exp_df[["Year", "Total_Expenditure"]],
    on="Year",
    how="inner"
)

# ----------------------
# DERIVED METRICS
# ----------------------
df["Fiscal Deficit"] = df["Total_Expenditure"] - df["Domestic Revenue"]

# Budget constraint components
df["Deficit Funded by Grants"] = df["Grants"].clip(lower=0)
df["Deficit Funded by Domestic Borrowing"] = df["Domestic Financing"].clip(lower=0)
df["Deficit Funded by Foreign Borrowing"] = df["Foreign Financing"].clip(lower=0)

df["Budget_RHS"] = df["Domestic Revenue"] + df["Deficit Funded by Grants"] + df["Deficit Funded by Domestic Borrowing"] + df["Deficit Funded by Foreign Borrowing"]
df["Budget_LHS"] = df["Total_Expenditure"]
df["Gap"] = df["Budget_LHS"] - df["Budget_RHS"]

# % composition of deficit funding
df["% Grants"] = df["Deficit Funded by Grants"] / df["Fiscal Deficit"] * 100
df["% Domestic Borrowing"] = df["Deficit Funded by Domestic Borrowing"] / df["Fiscal Deficit"] * 100
df["% Foreign Borrowing"] = df["Deficit Funded by Foreign Borrowing"] / df["Fiscal Deficit"] * 100

# Administration
def get_admin(year):
    if year <= 2011:
        return "MMD (2007–2011)"
    elif year <= 2021:
        return "PF (2011–2021)"
    else:
        return "UPND (2021–Present)"

df["Administration"] = df["Year"].apply(get_admin)

# ----------------------
# COMBINED REVENUE VS EXPENDITURE VS DEFICIT
# ----------------------
st.subheader("Revenue, Expenditure & Fiscal Deficit Over Time")
fig1 = px.line(
    df,
    x="Year",
    y=["Domestic Revenue", "Total_Expenditure", "Fiscal Deficit"],
    markers=True,
    title="Revenue vs Expenditure vs Fiscal Deficit"
)
st.plotly_chart(fig1, use_container_width=True)

# ----------------------
# BUDGET CONSTRAINT STACKED
# ----------------------
st.subheader("Budget Constraint (Stacked Funding vs Total Expenditure)")
funding_cols = ["Domestic Revenue", "Deficit Funded by Grants", "Deficit Funded by Domestic Borrowing", "Deficit Funded by Foreign Borrowing"]

fig2 = go.Figure()
for col in funding_cols:
    fig2.add_trace(go.Bar(
        x=df["Year"],
        y=df[col],
        name=col
    ))

# Overlay total expenditure
fig2.add_trace(go.Scatter(
    x=df["Year"],
    y=df["Total_Expenditure"],
    mode="lines+markers",
    name="Total Expenditure (LHS)",
    line=dict(color="red", width=3)
))

# Highlight where budget breaks (Expenditure > Funding)
gap_years = df[df["Gap"] > 0]
fig2.add_trace(go.Scatter(
    x=gap_years["Year"],
    y=gap_years["Total_Expenditure"],
    mode="markers",
    marker=dict(color="black", size=10, symbol="x"),
    name="Gap: Expenditure > Funding"
))

fig2.update_layout(
    title="Government Budget Constraint",
    xaxis_title="Year",
    yaxis_title="Amount (ZMW)",
    barmode='stack',
    legend_title="Components"
)
st.plotly_chart(fig2, use_container_width=True)

# ----------------------
# DEFICIT FUNDING COMPOSITION (%)
# ----------------------
st.subheader("Fiscal Deficit Funding Composition (%)")
composition_cols = ["% Grants", "% Domestic Borrowing", "% Foreign Borrowing"]
fig3 = px.bar(
    df,
    x="Year",
    y=composition_cols,
    title="Deficit Funding Composition by Source",
    labels={"value": "% of Deficit", "variable": "Funding Source"}
)
st.plotly_chart(fig3, use_container_width=True)

# ----------------------
# QUICK INSIGHTS
# ----------------------
st.subheader("📌 Quick Policy Insights")
latest_year = df["Year"].max()
latest = df.loc[df["Year"] == latest_year].iloc[0]

st.write(f"- Fiscal Deficit (Absolute) in {latest_year}: **{latest['Fiscal Deficit']:,.0f} ZMW**")
st.write(f"- Total Funding (Domestic Revenue + Grants + Borrowing): **{latest['Budget_RHS']:,.0f} ZMW**")
st.write(f"- Total Expenditure: **{latest['Total_Expenditure']:,.0f} ZMW**")
st.write(f"- Gap (Expenditure > Funding): **{latest['Gap']:,.0f} ZMW**")
st.write(f"- % of deficit funded by Grants: **{latest['% Grants']:.2f}%**")
st.write(f"- % of deficit funded by Domestic Borrowing: **{latest['% Domestic Borrowing']:.2f}%**")
st.write(f"- % of deficit funded by Foreign Borrowing: **{latest['% Foreign Borrowing']:.2f}%**")

# ----------------------
# RAW DATA DOWNLOAD
# ----------------------
st.subheader("Combined Dataset for Policy Analysis")
st.dataframe(df, use_container_width=True)
st.download_button(
    "Download Dataset",
    df.to_csv(index=False).encode("utf-8"),
    file_name="policy_analysis_combined.csv",
    mime="text/csv"
)
