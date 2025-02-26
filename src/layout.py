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
    save_filters_alert_message,
    analysis_name_input,
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
        dbc.Col(data_attribution, width="1", className="ms-2"),
        dbc.Col([
            dbc.Row([
                dbc.Col(region_dropdown, width="3"),
                dbc.Col(year_dropdown, width="3"),
                dbc.Col(analysis_name_input, width="4"),
                dbc.Col(dbc.ButtonGroup([save_filters_button, save_filters_tooltip, save_filters_alert_message]), width="auto")
            ], justify="center", align="items-center", className="g-2")
        ], width={"size": "8", "offset": 0.5}),
        dbc.Col(dbc.ButtonGroup([clear_button, clear_button_tooltip]), width="auto", className="me-2")
    ], justify="between", align="items-center", className="g-0"),


    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(dcc.Loading(id='bar-chart-card-content')),
                className="chart-card top-chart-card",
            ),
            width=6,
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(dcc.Loading(id='pie-chart-card-content')), 
                className="chart-card top-chart-card"
            ),
            width=6,
        )
    ]),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dcc.Loading(id='disparity-map-card-content'),
                    occupation_type_slider
                ])
            ], className="chart-card bottom-chart-card"),
            width=6,
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(dcc.Loading(id='stacked-area-chart-card-content')),
                className="chart-card bottom-chart-card"
            ),
            width=6,
        )
    ]),

    dbc.Row([
        dbc.Col(summary_stats),  # Add summary_stats component
    ]),

    dcc.Store(id='saved-analyses-store', data=[])
])