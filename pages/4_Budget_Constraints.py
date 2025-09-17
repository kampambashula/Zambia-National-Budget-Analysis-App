import streamlit as st
import pandas as pd
from utils.helpers import load_budget_data

st.title("📉 Budget Constraints")

data = load_budget_data()

if data is not None:
    st.subheader("Deficit and Debt Dynamics")

    st.line_chart(data.set_index("Year")[["Deficit", "Debt_to_GDP"]])

    st.markdown("### Budget Constraint Formula (Basic)")
    st.latex(r"""
        G_t + i \cdot B_{t-1} = T_t + \Delta B_t
    """)

    st.markdown(
        """
        Where:  
        - \( G_t \): Government spending  
        - \( i \): Interest rate on debt  
        - \( B_{t-1} \): Previous debt stock  
        - \( T_t \): Government revenues  
        - \( \Delta B_t \): Change in borrowing (new debt)   # type: ignore
        """
    )

    st.info("Later we can extend this with Zambia-specific fiscal data for more accurate constraints.")
else:
    st.warning("Upload or fill `data/budget_data.csv` to see results.")
