import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Macroeconomic Fundamentals")

# --- Load Data ---
file_path = "econ/all.csv"  # path to your compiled dataset

try:
    data = pd.read_csv(file_path)

    # Clean column names (remove spaces & trailing characters)
    data.columns = data.columns.str.strip()

    # --- GDP Growth ---
    if "GDP growth (annual %)" in data.columns:
        fig_gdp = px.line(
            data,
            x="Year",
            y="GDP growth (annual %)",
            title="📊 GDP Growth Over Time",
            markers=True
        )
        st.plotly_chart(fig_gdp, use_container_width=True)

        st.markdown(
            """
            **Commentary:**  
            GDP growth shows how Zambia’s economy has expanded or contracted over time.  
            Periods of sharp growth often reflect favorable copper prices, good rainfall (boosting agriculture),  
            or strong investment. Declines usually signal global shocks, fiscal stress, or local challenges.  
            """
        )

    # --- Inflation ---
    if "Inflation, consumer prices (annual %)" in data.columns:
        fig_inflation = px.line(
            data,
            x="Year",
            y="Inflation, consumer prices (annual %)",
            title="💹 Inflation Over Time",
            markers=True,
            line_shape="spline"
        )
        st.plotly_chart(fig_inflation, use_container_width=True)

        st.markdown(
            """
            **Commentary:**  
            Inflation reflects how quickly consumer prices are rising.  
            High inflation typically reduces purchasing power and can discourage savings,  
            while low and stable inflation is supportive of long-term planning and investment.  
            Look for periods where inflation spikes – these may align with exchange rate volatility  
            or rising global food and fuel prices.  
            """
        )

    # --- Debt Stock ---
    if "Total Debt stock" in data.columns:
        fig_debt = px.line(
            data,
            x="Year",
            y="Total Debt stock",
            title="💰 Total Debt Stock Over Time",
            markers=True
        )
        st.plotly_chart(fig_debt, use_container_width=True)

        st.markdown(
            """
            **Commentary:**  
            Debt stock indicates Zambia’s total obligations to creditors.  
            Rising debt levels may suggest more government borrowing to finance spending,  
            but rapid increases relative to GDP can raise sustainability concerns.  
            Watch how debt trends line up with GDP growth — ideally, the economy grows  
            faster than debt to maintain a healthy balance.  
            """
        )

except FileNotFoundError:
    st.warning("⚠️ `all.csv` not found. Please make sure the file is in the project folder.")
