import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# =========================
# Load Data
# =========================
def load_expenditure_data():
    df = pd.read_csv("csv_output/EXPENDITURE.csv", encoding="latin-1")

    # Clean column names
    df.columns = df.columns.str.strip().str.replace('"', '').str.replace("\n", " ")
    df["Year"] = df["Year"].astype(int)

    # Clean numeric values: remove commas/spaces and convert to numbers
    for col in df.columns:
        if col != "Year":  # don't touch the Year column
            df[col] = (
                df[col]
                .astype(str)                  # ensure string type
                .str.replace(",", "")         # remove commas
                .str.replace(" ", "")         # remove spaces
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.sort_values("Year")
    return df

df = load_expenditure_data()

# =========================
# Define Government Periods
# =========================
def assign_government(year):
    if 2007 <= year <= 2011:
        return "MMD (2007-2011)"
    elif 2012 <= year <= 2021:
        return "PF (2011-2021)"
    elif 2022 <= year <= 2025:
        return "UPND (2021- )"
    else:
        return "Other"

df["Government"] = df["Year"].apply(assign_government)

# =========================
# Election Year Helper
# =========================
ELECTION_YEARS = [2011, 2016, 2021, 2026]

def add_election_markers(fig):
    """Add vertical dashed lines for Zambian election years"""
    for year in ELECTION_YEARS:
        fig.add_vline(
            x=year,
            line_width=2,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Election {year}",
            annotation_position="top"
        )
    return fig

# =========================
# Streamlit Layout
# =========================
st.title("💰 Zambia Expenditure Analysis (2007–2025)")

st.markdown("""
We analyze Zambia’s **government expenditure trends** across three administrations:  
- **MMD (2007–2011)**  
- **PF (2012–2021)**  
- **UPND (2022–Present)**  

Election years (2011, 2016, 2021, 2026) are marked with **red dashed lines** for context.  
""")

# =========================
# Total Expenditure Over Time
# =========================
st.subheader("Total Expenditure Over Time")

fig_total = px.line(
    df,
    x="Year",
    y="Total_Expenditure",
    color="Government",
    markers=True,
    title="Total Expenditure (2007–2025)",
    labels={"Total_Expenditure": "Total Expenditure (ZMW)"}
)
fig_total = add_election_markers(fig_total)
st.plotly_chart(fig_total, use_container_width=True)

# =========================
# Major Sectors Over Time
# =========================
st.subheader("Expenditure by Major Sector")

major_sectors = [
    "General Public Services",
    "Defence",
    "Public Order and Safety",
    "Economic Affairs",
    "Environmental Protection",
    "Housing and Community Amenities",
    "Health",
    "Recreation, Culture and Religion",
    "Education",
    "Social Protection"
]

df_long = df.melt(
    id_vars=["Year", "Government", "Total_Expenditure"], 
    value_vars=major_sectors, 
    var_name="Sector", 
    value_name="Expenditure"
)

fig_sector = px.line(
    df_long,
    x="Year",
    y="Expenditure",
    color="Sector",
    hover_name="Sector",
    markers=True,
    title="Major Sector Expenditure Trends (2007–2025)",
    labels={"Expenditure": "Expenditure (ZMW)"}
)
fig_sector = add_election_markers(fig_sector)
st.plotly_chart(fig_sector, use_container_width=True)

# =========================
# Sector Shares (% of Total)
# =========================
st.subheader("Sector Shares of Total Expenditure")

df_long["Share"] = df_long["Expenditure"] / df_long["Total_Expenditure"] * 100

fig_share_area = px.area(
    df_long,
    x="Year",
    y="Share",
    color="Sector",
    groupnorm="percent",
    title="Sector Share of Total Expenditure Over Time (%)",
    labels={"Share": "Share of Total Expenditure (%)"}
)
fig_share_area = add_election_markers(fig_share_area)
st.plotly_chart(fig_share_area, use_container_width=True)

# =========================
# Key Sub-Categories
# =========================
st.subheader("🔎 Focus on Key Sub-Categories")

sub_categories = [
    "Domestic Debt",
    "External Debt (Interest and Principal)",
    "Road Infrastructure",
    "Farmer Input Support",
    "Strategic Food Reserve",
    "Social Cash Transfer"
]

df_sub = df.melt(
    id_vars=["Year", "Government", "Total_Expenditure"], 
    value_vars=sub_categories, 
    var_name="SubCategory", 
    value_name="Expenditure"
)

fig_sub = px.line(
    df_sub,
    x="Year",
    y="Expenditure",
    color="SubCategory",
    markers=True,
    title="Critical Sub-Category Expenditure Trends (2007–2025)",
    labels={"Expenditure": "Expenditure (ZMW)"}
)
fig_sub = add_election_markers(fig_sub)
st.plotly_chart(fig_sub, use_container_width=True)

# =========================
# Sub-Category Shares
# =========================
st.subheader("Sub-Category Shares of Total Expenditure (%)")

df_sub["Share"] = df_sub["Expenditure"] / df_sub["Total_Expenditure"] * 100

fig_sub_share = px.area(
    df_sub,
    x="Year",
    y="Share",
    color="SubCategory",
    groupnorm="percent",
    title="Sub-Category Share of Total Expenditure (%)",
    labels={"Share": "Share (%)"}
)
fig_sub_share = add_election_markers(fig_sub_share)
st.plotly_chart(fig_sub_share, use_container_width=True)

# =========================
# Interactive Sector/Sub-Category Focus
# =========================
st.subheader("🎯 Explore a Specific Sector or Sub-Category")

focus_choice = st.selectbox("Choose a Sector or Sub-Category:", major_sectors + sub_categories)
df_focus = df.melt(
    id_vars=["Year", "Government", "Total_Expenditure"], 
    value_vars=[focus_choice], 
    var_name="Item", 
    value_name="Expenditure"
)

fig_focus = px.bar(
    df_focus,
    x="Year",
    y="Expenditure",
    color="Government",
    title=f"{focus_choice} Expenditure (2007–2025)",
    labels={"Expenditure": "Expenditure (ZMW)"}
)
fig_focus = add_election_markers(fig_focus)
st.plotly_chart(fig_focus, use_container_width=True)

# =========================
# Insights
# =========================
st.subheader("Insights & Commentary")

st.markdown("""
- **Election years (2011, 2016, 2021, 2026)** show spikes in politically sensitive spending like **FISP, roads, and reserves**.  
- **PF years** feature sustained investment in **Road Infrastructure** — consistent with their campaign priorities.  
- **UPND years** show higher allocations to **Social Cash Transfers and Health**, reflecting social contract commitments.  
- **Debt servicing** rises continuously, limiting fiscal space regardless of government.  
""")
