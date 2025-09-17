import streamlit as st
from utils.loaders import load_revenue, load_expenditure, load_debt, load_macro
from utils.metrics import compute_deficit_gdp, compute_debt_gdp

st.title("📊 Budget Snapshot")

revenue = load_revenue()
expenditure = load_expenditure()
debt = load_debt()
macro = load_macro()

latest = revenue["year"].max()
rev = revenue[revenue.year == latest].total_revenue.values[0]
exp = expenditure[expenditure.year == latest].total_expenditure.values[0]
gdp = macro[macro.year == latest].gdp.values[0]
debt_stock = debt[debt.year == latest].debt_stock.values[0]

st.metric("Deficit/GDP", f"{compute_deficit_gdp(rev, exp, gdp):.1%}")
st.metric("Debt/GDP", f"{compute_debt_gdp(debt_stock, gdp):.1%}")
