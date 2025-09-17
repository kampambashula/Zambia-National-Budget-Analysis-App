import pandas as pd

def load_budget_data():
    try:
        return pd.read_csv("data/budget_data.csv")
    except FileNotFoundError:
        return None
