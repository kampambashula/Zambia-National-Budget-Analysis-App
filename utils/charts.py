import plotly.express as px

def plot_sector_allocations(df):
    sectors = ["health", "education", "agriculture", "infrastructure", "social_protection"]
    fig = px.bar(df, x="year", y=sectors, title="Sector Allocations (K)", barmode="stack")
    return fig
