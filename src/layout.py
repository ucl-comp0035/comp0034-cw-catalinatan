from dash import dcc, html
import dash_bootstrap_components as dbc
from components import (
    region_dropdown,
    year_dropdown,
    occupation_type_slider,
    clear_button,
    save_filters_button
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
        dbc.Col(html.P("Selection filters"), width=2),
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
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4("Gender Disparity Statistics", className="text-center")),
                dbc.CardBody([
                    html.H1(["Summary Statistics for ", html.Span(id='selected-region'), " in ", html.Span(id='selected-year')]),
                    dbc.Row([
                        dbc.Col([
                            html.H5("Highest Overall Gender Disparity for the Year", className="mb-3"),
                            dbc.Card([
                                dbc.CardBody([
                                    html.P(["Region: ", html.Span(id='highest-disparity-region')], className="mb-0 text-muted"),
                                    html.P(["Disparity: ", html.Span(id='highest-disparity-percentage')], className="text-danger"),
                                ])
                            ], className="mb-3 shadow-sm")
                        ], md=6),
                        dbc.Col([
                            html.H5("Highest Disparity by Occupation", className="mb-3"),
                            dbc.Card([
                                dbc.CardBody([
                                    html.P(["Occupation: ", html.Span(id='highest-disparity-occupation')], className="mb-0 text-muted"),
                                    html.P(["Disparity: ", html.Span(id='highest-disparity-occupation-percentage')], className="text-danger"),
                                ])
                            ], className="mb-3 shadow-sm")
                        ], md=6)
                    ]),
                    html.H5("Highest Employment % by Gender", className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader(html.H6("Male", className="mb-0")),
                                dbc.CardBody([
                                    html.P(["Occupation: ", html.Span(id='highest-male-employment-occupation')], className="mb-0 text-muted"),
                                    html.P(["Percentage: ", html.Span(id='highest-male-employment-percentage')], className="text-primary"),
                                ])
                            ], className="shadow-sm")
                        ], md=6),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader(html.H6("Female", className="mb-0")),
                                dbc.CardBody([
                                    html.P(["Occupation: ", html.Span(id='highest-female-employment-occupation')], className="mb-0 text-muted"),
                                    html.P(["Percentage: ", html.Span(id='highest-female-employment-percentage')], className="mb-0 text-primary"),
                                ])
                            ], className="shadow-sm")
                        ], md=6)
                    ]),
                ])
            ], className="shadow")
        )
    ]),


    dcc.Store(id='saved-analyses-store', data=[])
])