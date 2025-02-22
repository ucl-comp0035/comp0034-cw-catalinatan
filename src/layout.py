from dash import dcc, html
import dash_bootstrap_components as dbc
from components import (
    region_dropdown,
    year_dropdown,
    occupation_type_slider,
    clear_button,
    save_filters_button, 
    display_summary_button,
    summary_stats  # Import summary_stats
)

# Define the layout of the app
app_layout = dbc.Container([
    dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                children=[],
                nav=True,
                in_navbar=True,
                label="Saved Analyses",
                id="saved-analyses-menu"
            ),
        ],
        brand="Comparative Employment Analysis Tool",
        color="#4292C3",
        dark=True
    ),

    dbc.Row([
        dbc.Col(display_summary_button, width=2),
        dbc.Col(region_dropdown, width=3),
        dbc.Col(year_dropdown, width=3),
        dbc.Col(save_filters_button),
        dbc.Col(clear_button)
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
    ]),

    dbc.Row([
        dbc.Col(summary_stats),  # Add summary_stats component
    ]),

    dcc.Store(id='saved-analyses-store', data=[])
])