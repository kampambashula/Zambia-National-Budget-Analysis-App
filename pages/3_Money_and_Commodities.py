import streamlit as st
import pandas as pd
import plotly.express as px

st.title("💰 Money & Commodities")

# --- Load Data ---
file_path = "econ/all.csv"

try:
    df = pd.read_csv(file_path)

    # Clean column names
    df.columns = df.columns.str.strip()

    # --- Money Supply ---
    st.subheader("Money Supply")
    money_cols = ["Narrow Money", "Broad Money (M2)***", "Broad Money (M3)"]
    money_cols = [col for col in money_cols if col in df.columns]

    if money_cols:
        df_money = df[["Year"] + money_cols].dropna()
        fig_money = px.line(
            df_money,
            x="Year",
            y=money_cols,
            markers=True,
            title="Money Supply Over Time"
        )
        st.plotly_chart(fig_money, use_container_width=True)
        st.markdown(
            """
            **Commentary:**  
            Broad money (M2 and M3) growing faster than narrow money suggests a rapid expansion of deposits beyond cash in circulation.  
            If not matched by economic growth, this can exert upward pressure on inflation.
            """
        )

    # --- Individual Commodity Graphs ---
    commodity_mapping = {
        "Copper US /Tonne": "Copper Prices Over Time",
        "Cobalt US$/Tonne": "Cobalt Prices Over Time",
        "Crude Oil US$/barrel": "Crude Oil Prices Over Time",
        "Maize (K'/50Kg)": "Maize Prices Over Time"
    }

    for col, title in commodity_mapping.items():
        if col in df.columns:
            df_commodity = df[["Year", col]].dropna()
            fig = px.line(
                df_commodity,
                x="Year",
                y=col,
                markers=True,
                title=title
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"**Commentary:** {title} show how {col.split()[0]} prices have evolved over time. "\
                        "Tracking these helps understand export earnings, domestic inflation, and commodity market trends.")

except FileNotFoundError:
    st.error("⚠️ `all.csv` not found. Please make sure the file is in the `econ` folder.")
