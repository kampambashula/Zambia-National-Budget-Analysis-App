import streamlit as st
import pandas as pd
from utils.helpers import load_budget_data

st.title("🔄 Priority Shifts")

data = load_budget_data()

if data is not None:
    st.subheader("Sector Priority Changes Over Time")

    # Select years to compare
    years = data["Year"].tolist()
    year1 = st.selectbox("Select first year", years, index=0)
    year2 = st.selectbox("Select comparison year", years, index=len(years)-1)

    if year1 != year2:
        df1 = data[data["Year"] == year1]
        df2 = data[data["Year"] == year2]

        st.write(f"Comparing allocations between {year1} and {year2}")

        # Calculate changes
        sectors = ["Health", "Education", "Infrastructure", "Agriculture", "Social_Protection"]
        comparison = pd.DataFrame({
            "Sector": sectors,
            f"Allocation {year1}": [df1[s].values[0] for s in sectors],
            f"Allocation {year2}": [df2[s].values[0] for s in sectors],
            "Change (%)": [
                round(((df2[s].values[0] - df1[s].values[0]) / df1[s].values[0]) * 100, 2)
                for s in sectors
            ]
        })

        st.dataframe(comparison)
        st.bar_chart(comparison.set_index("Sector")[["Change (%)"]])
    else:
        st.warning("Please select two different years for comparison.")
else:
    st.warning("Upload or fill `data/budget_data.csv` to see results.")
