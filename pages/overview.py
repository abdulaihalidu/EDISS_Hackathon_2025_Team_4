import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div([
    html.H2("Overview"),
    html.P("The EHS AI-Based Pallet Stacking and Transportation System ensures safe stacking and efficient logistics."),
])
