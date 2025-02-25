from dash import dcc, html
import dash_bootstrap_components as dbc
from components import (
    region_dropdown,
    year_dropdown,
    occupation_type_slider,
    clear_button,
    clear_button_tooltip,
    save_filters_button, 
    save_filters_tooltip,
    data_attribution,
    summary_stats # Import summary_stats
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
        brand_style={"font-weight": "bold"},
        color="#4292C3",
        dark=True,
        style={"margin-bottom": "20px"}
    ),

    dbc.Row([
        dbc.Col(data_attribution, width=1),
        dbc.Col(region_dropdown, width=3),
        dbc.Col(year_dropdown, width=3),
        dbc.Col([save_filters_button, save_filters_tooltip]),
        dbc.Col([clear_button, clear_button_tooltip])
    ]),

    dbc.Row([
        dbc.Col(
            dbc.Card(dcc.Graph(id='stacked-bar-chart'), body=True, className="chart-card top-chart-card"),
            width=6,
        ),
        dbc.Col(
            dbc.Card(dcc.Graph(id='pie-chart'), body=True, className="chart-card top-chart-card"), 
            width=6
        )
    ]),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dcc.Graph(id='disparity-map'),
                occupation_type_slider
            ], className="chart-card bottom-chart-card", body=True),
            width=6,
        ),
        dbc.Col(
            dbc.Card(dcc.Graph(id='stacked-area-chart'), body=True, className="chart-card bottom-chart-card"),
            width=6,
        )
    ]),

    dbc.Row([
        dbc.Col(summary_stats),  # Add summary_stats component
    ]),

    dcc.Store(id='saved-analyses-store', data=[])
])