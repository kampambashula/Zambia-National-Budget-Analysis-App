import streamlit as st

# Page configuration
st.set_page_config(page_title="Zambia Budget Analysis - BudgetPulse Zambia", layout="wide")

# --- Cover Image / Banner ---
st.image(
    "https://img.freepik.com/free-vector/financial-data-analytics-banner-template_1017-31728.jpg",
    use_column_width=True,
    caption="Zambia National Budget 2026 - Analysis Dashboard"
)

# Main Title
st.title("📊 Zambia National Budget Analysis App")

st.markdown(
    """
    Welcome to the **Zambia National Budget Analysis Dashboard**.  
    This platform provides real-time insights into the national budget with a focus on the **2026 budget**.  
    Use the sidebar to navigate across different sections of the analysis.
    """
)

# --- Create Columns for Navigation Cards ---
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

# Footer note
st.markdown("---")
st.caption("Developed by Kampamba Shula · Powered by Streamlit")
