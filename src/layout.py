from dash import dcc, html
import dash_bootstrap_components as dbc
from components import (
    region_dropdown,
    year_dropdown,
    occupation_type_slider,
    clear_button
)

# Define the layout of the app
app_layout = dbc.Container([
    dbc.NavbarSimple(
        brand="Comparative Employment Analysis Tool",
        color="#4292C3",
        dark=True
    ),

    dbc.Row([
        dbc.Col(html.P("Selection filters"), width=2),
        dbc.Col(region_dropdown, width=4),
        dbc.Col(year_dropdown, width=4),
        dbc.Col(clear_button, width=2)
    ]),

    dbc.Row([
        dbc.Col(
            dbc.Card(dcc.Graph(id='stacked-bar-chart'), body=True),
            width=6
        ),
        dbc.Col(dbc.Card(dcc.Graph(id='pie-chart'), body=True), width=6)
    ]),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dcc.Graph(id='disparity-map'),
                occupation_type_slider
            ]),
            width=6
        ),
        dbc.Col(
            dbc.Card(dcc.Graph(id='stacked-area-chart'), body=True),
            width=6
        )
    ])
])