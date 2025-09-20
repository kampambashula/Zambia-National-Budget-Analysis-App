# revenue.py

import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------
# PAGE CONFIG
# ----------------------
st.set_page_config(page_title="Revenue Analysis", layout="wide")

st.title("📊 Zambia Budget Revenue Analysis (2007–2025)")

# ----------------------
# LOAD DATA
# ----------------------
@st.cache_data
def load_data():
    df = pd.read_csv("csv_output/REVENUE.csv", encoding="latin1")
    df.columns = df.columns.str.strip().str.replace('"', '').str.replace("\n", " ")
    df["Year"] = df["Year"].astype(int)
    df = df.sort_values("Year")
    return df

df = load_data()


# ----------------------
# COMPUTE POLICY RATIOS
# ----------------------
df["Tax/Total Revenue (%)"] = (df["Tax Revenue"] / df["Domestic Revenue"]) * 100
df["Mineral/Total Revenue (%)"] = (df["Mineral Royalty"] / df["Domestic Revenue"]) * 100
df["Grants/Total Revenue (%)"] = (df["Grants"] / df["Domestic Revenue"]) * 100
df["Domestic vs Foreign Financing (%)"] = (df["Domestic Financing"] / df["GROSS FINANCING"]) * 100

# For stacked chart
financing_df = df[["Year", "Domestic Financing", "Foreign Financing"]].melt(
    id_vars="Year", var_name="Financing Source", value_name="Amount"
)

# ----------------------
# SELECT VISUALIZATION
# ----------------------
st.sidebar.header("Filters")
viz_type = st.sidebar.selectbox(
    "Select Visualization",
    [
        "Revenue Trends",
        "Tax Revenue Breakdown",
        "Non-Tax Revenue Breakdown",
        "Grants & Financing",
        "Domestic vs Foreign Financing Mix",
        "Policy Ratios",
        "Raw Data"
    ]
)

# ----------------------
# VISUALIZATIONS
# ----------------------

if viz_type == "Revenue Trends":
    fig = px.line(
        df,
        x="Year",
        y=["Domestic Revenue", "Tax Revenue", "Non-Tax Revenue"],
        markers=True,
        title="Revenue Trends Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)

elif viz_type == "Tax Revenue Breakdown":
    tax_cols = [
        "Income Tax", "Company Tax", "Pay as You Earn (PAYE)",
        "Withholding Tax and Other", "Value Added Tax (VAT)",
        "Customs Duties", "Excise Duties"
    ]
    fig = px.line(
        df, x="Year", y=tax_cols, markers=True,
        title="Tax Revenue Components Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)

elif viz_type == "Non-Tax Revenue Breakdown":
    non_tax_cols = [
        "Mineral Royalty", "Motor Vehicle Fees", "Tourism Levy",
        "Skills Development Levy", "Insurance Premium Levy"
    ]
    fig = px.line(
        df, x="Year", y=non_tax_cols, markers=True,
        title="Non-Tax Revenue Components Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)

elif viz_type == "Grants & Financing":
    financing_cols = [
        "Grants", "Project Grants", "Programme Grants",
        "GROSS FINANCING", "Domestic Financing", "Foreign Financing"
    ]
    fig = px.line(
        df, x="Year", y=financing_cols, markers=True,
        title="Grants and Financing Trends"
    )
    st.plotly_chart(fig, use_container_width=True)

elif viz_type == "Domestic vs Foreign Financing Mix":
    fig = px.bar(
        financing_df,
        x="Year",
        y="Amount",
        color="Financing Source",
        title="Domestic vs Foreign Financing Mix (Stacked)",
        barmode="stack"
    )
    st.plotly_chart(fig, use_container_width=True)

elif viz_type == "Policy Ratios":
    ratio_cols = [
        "Tax/Total Revenue (%)",
        "Mineral/Total Revenue (%)",
        "Grants/Total Revenue (%)",
        "Domestic vs Foreign Financing (%)"
    ]
    fig = px.line(
        df, x="Year", y=ratio_cols, markers=True,
        title="Policy-Relevant Ratios"
    )
    st.plotly_chart(fig, use_container_width=True)

elif viz_type == "Raw Data":
    st.dataframe(df, use_container_width=True)
    st.download_button(
        "Download CSV with Ratios",
        df.to_csv(index=False).encode("utf-8"),
        file_name="revenue_with_ratios.csv",
        mime="text/csv"
    )

# ----------------------
# SUMMARY
# ----------------------
st.write("### Quick Insights")
st.write(f"- Latest year in dataset: **{df['Year'].max()}**")
st.write(f"- Tax Revenue (2025): **{df.loc[df['Year']==2025, 'Tax Revenue'].values[0]:,.0f} ZMW**")
st.write(f"- Mineral Royalty as % of Domestic Revenue (2025): **{df.loc[df['Year']==2025, 'Mineral/Total Revenue (%)'].values[0]:.2f}%**")
st.write(f"- Grants as % of Domestic Revenue (2025): **{df.loc[df['Year']==2025, 'Grants/Total Revenue (%)'].values[0]:.2f}%**")
