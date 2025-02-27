import dash
from dash import html, Input, Output
import requests
import json

dash.register_page(__name__, path="/safety")

BACKEND_URL = "http://localhost:8000"

layout = html.Div([
    html.H2("Safety Checks"),
    html.Button("Perform Safety Check", id="safety-check", n_clicks=0),
    html.Div(id="safety-output")
])

@dash.callback(
    Output("safety-output", "children"),
    Input("safety-check", "n_clicks")
)
def perform_safety_check(n_clicks):
    if n_clicks > 0:
        response = requests.get(f"{BACKEND_URL}/safety-check")
        if response.status_code == 200:
            data = response.json()
            return html.Pre(json.dumps(data, indent=2))
    return "Click to perform a safety check."
