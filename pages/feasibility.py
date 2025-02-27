import dash
from dash import html, Input, Output
import requests
import json

dash.register_page(__name__, path="/feasibility")

BACKEND_URL = "http://localhost:8000"

layout = html.Div([
    html.H2("Feasibility Study"),
    html.Button("Fetch Study Data", id="fetch-feasibility", n_clicks=0),
    html.Div(id="feasibility-output")
])

@dash.callback(
    Output("feasibility-output", "children"),
    Input("fetch-feasibility", "n_clicks")
)
def fetch_feasibility(n_clicks):
    if n_clicks > 0:
        response = requests.get(f"{BACKEND_URL}/feasibility")
        if response.status_code == 200:
            data = response.json()
            return html.Pre(json.dumps(data, indent=2))
    return "Click to fetch feasibility study results."
