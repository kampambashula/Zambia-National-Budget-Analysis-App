import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Zambia Budget Analysis - BudgetPulse Zambia",
    layout="wide"
)

# --- Load Data ---
df = pd.read_csv("econ/all.csv")

# Make sure Year is integer for easier indexing
df["Year"] = df["Year"].astype(int)

# Get the latest year snapshot
latest_year = df["Year"].max()
snapshot = df[df["Year"] == latest_year].squeeze()

# Main Title
st.title("📊 Zambia National Budget Analysis App")

st.markdown(
    f"""
    Welcome to the **Zambia National Budget Analysis Dashboard**.  
    This platform provides real-time insights into the national budget with a focus on the **{latest_year} snapshot**.  
    Use the sidebar to navigate across different sections of the analysis.
    """
)

# --- Snapshot Metrics ---
st.subheader(f"📌 Key Economic Indicators ({latest_year})")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Inflation (CPI, %)",
        value=f"{snapshot['Inflation, consumer prices (annual %)']:.2f}%"
    )

with col2:
    st.metric(
        label="GDP Growth (%)",
        value=f"{snapshot['GDP growth (annual %)']:.2f}%"
    )

with col3:
    st.metric(
        label="Unemployment (%)",
        value=f"{snapshot['Unemployment, total (% of total labor force)']:.2f}%"
    )

with col4:
    st.metric(
        label="Total Debt Stock",
        value=f"${snapshot['Total Debt stock']:,.0f}"
    )

# --- Navigation Cards ---
st.subheader("🔍 Explore Analysis Pages")

col1, col2, col3 = st.columns(3)
col4, col5, _ = st.columns([1,1,1])

with col1:
    st.markdown("### 📈 Macroeconomic Fundamentals")
    st.info("Explore GDP growth, inflation, fiscal deficit, and debt-to-GDP ratios.")

with col2:
    st.markdown("### 🏥📚 Sector Allocations")
    st.info("See how the budget is distributed across health, education, infrastructure, and more.")

with col3:
    st.markdown("### 🔄 Priority Shifts")
    st.info("Track how government priorities shift between sectors across years.")

with col4:
    st.markdown("### 📉 Budget Constraints")
    st.info("Understand fiscal constraints, deficits, and debt dynamics.")

with col5:
    st.markdown("### 🌍 Comparative Analysis")
    st.info("Visualize long-term trends and compare allocations over time.")

# Footer
st.markdown("---")
st.caption("Developed by Kampamba Shula · Powered by Streamlit")
