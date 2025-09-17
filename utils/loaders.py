import pandas as pd

def load_revenue(path="data/revenue.csv"):
    return pd.read_csv(path)

def load_expenditure(path="data/expenditure.csv"):
    return pd.read_csv(path)

def load_debt(path="data/debt.csv"):
    return pd.read_csv(path)

def load_macro(path="data/macro.csv"):
    return pd.read_csv(path)
