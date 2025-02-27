import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import requests
import pandas as pd

dash.register_page(__name__, path="/analytics")

BACKEND_URL = "http://localhost:8000"

layout = html.Div([
    html.H2("Data Analytics"),
    dcc.Graph(id="analytics-graph"),
    html.Button("Load Analytics Data", id="load-analytics", n_clicks=0)
])

@dash.callback(
    Output("analytics-graph", "figure"),
    Input("load-analytics", "n_clicks")
)
def load_analytics(n_clicks):
    if n_clicks > 0:
        response = requests.get(f"{BACKEND_URL}/analytics")
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            fig = px.bar(df, x="time", y="stacking_efficiency", title="Stacking Efficiency Over Time")
            return fig
    return px.bar(title="No Data Yet")
