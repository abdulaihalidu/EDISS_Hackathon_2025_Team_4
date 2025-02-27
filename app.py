import dash
from dash import html, dcc
import dash_bootstrap_components as dbc  

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

# Define Navbar
navbar = dbc.NavbarSimple(
    brand="EHS AI-Based Pallet Stacking & Transportation System",
    brand_href="/",
    color="dark",
    dark=True,
    children=[
        dbc.NavItem(dcc.Link("Overview", href="/", className="nav-link")),
        dbc.NavItem(dcc.Link("Real-Time Monitoring", href="/monitoring", className="nav-link")),
        dbc.NavItem(dcc.Link("Data Analytics", href="/analytics", className="nav-link")),
        dbc.NavItem(dcc.Link("Safety Checks", href="/safety", className="nav-link")),
        dbc.NavItem(dcc.Link("Feasibility Study", href="/feasibility", className="nav-link")),
    ],
)

# Define App Layout
app.layout = dbc.Container([
    navbar,  # Navigation bar
    html.Br(),
    dbc.Card(
        dbc.CardBody([
            dash.page_container  # Dynamic content
        ]),
        className="shadow p-4",
    )
], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)
