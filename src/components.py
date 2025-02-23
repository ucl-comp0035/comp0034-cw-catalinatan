from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
from pathlib import Path
# import dash-daq as daq
from filter_data_functions import (
    highest_m_year_disparity_percentage,
    highest_m_year_disparity_occupation,
    highest_m_year_disparity_region, 
    highest_f_year_disparity_percentage,
    highest_f_year_disparity_occupation,
    highest_f_year_disparity_region)

# Dropdowns for region, year and occupation
region_dropdown = dcc.Dropdown(
    options=['England', 'Wales', 'Scotland', 'Northern Ireland'],
    value=None,
    id='region-dropdown',
    placeholder='Select a region'
)

year_dropdown = dcc.Dropdown(
    options=['2021', '2022', '2023'],
    value=None,
    id='year-dropdown',
    placeholder='Select a year',
)

occupation_marks = {i: str(i) for i in range(1, 10)}

full_descriptions = {
    1: "Managers, directors and senior officials",
    2: "Professional occupations",
    3: "Associate prof & tech occupations",
    4: "Administrative and secretarial occupations",
    5: "Skilled trades occupations",
    6: "Caring, leisure and other service occupations",
    7: "Sales and customer service occupations",
    8: "Process, plant and machine operatives",
    9: "Elementary occupations"
}

# Occupation type slider
occupation_type_slider = html.Div([
    html.Div([
        dbc.Label("Select a occupation type"),
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'marginBottom': '8px'
    }),
    dcc.Slider(
        min=1,
        max=9,
        step=1,
        marks=occupation_marks,
        value=1,
        id='occupation-type-slider',
        tooltip={
            "placement": "bottom",
            "always_visible": True,
            "template": "{full_description}"
        },
        included=False,
    )
], style={'display': 'flex', 'flexDirection': 'column'})

# Clear button
clear_button = html.Button('Clear selections', id='clear-button', n_clicks=0)

# Save filters button 
save_filters_button = html.Button('Save filters', id='save-filters-button', n_clicks=0)

# Display summary statistics button
display_summary_button = html.Button('Summary Statistics',id='display-summary-button', n_clicks=0)

# Summmary Gender Disparity Statistics
gender_disparity_stats = dbc.Card([
    dbc.CardHeader(html.H4("Gender Disparity Statistics", className="text-center")),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.H5("Greatest Gender Disparity for the Year (Overall)", className="mb-3"),
                dbc.Card([
                    dbc.CardBody([
                        html.P(["Region: ", html.Span(id='highest-disparity-region')], className="mb-0 text-muted"),
                        html.P(["Disparity: ", html.Span(id='highest-disparity-percentage')], className="text-danger"),
                    ])
                ], className="mb-3 shadow-sm")
            ], md=6)
        ]),
        html.H1(["For ", html.Span(id='selected-region'), " in ", html.Span(id='selected-year')]),
        dbc.Row([
            dbc.Col([
                html.H5("Greatest Disparity by Occupation", className="mb-3"),
                dbc.Card([
                    dbc.CardBody([
                        html.P(["Occupation: ", html.Span(id='highest-disparity-occupation')], className="mb-0 text-muted"),
                        html.P(["Disparity: ", html.Span(id='highest-disparity-occupation-percentage')], className="text-danger"),
                    ])
                ], className="mb-3 shadow-sm")
            ], md=6)
        ]),
    ])
])

# Occupation Statistics
occupation_stats = dbc.Card([
    dbc.CardHeader(html.H4("Occupation Statistics", className="text-center")),
    dbc.CardBody([
        html.H1(["For ", html.Span(id='selected-region'), " in ", html.Span(id='selected-year')]),
        html.H5("Highest Employment Percentage (%)", className="mb-3"),
        dbc.Row([
            dbc.Card([
                dbc.CardHeader(html.H6("Overall", className="mb-0")),
                dbc.CardBody([
                    html.P(["Occupation Type: ", html.Span(id='highest-employment-occupation')], className="mb-0 text-muted"),
                    html.P(["Percentage (%): ", html.Span(id='highest-employment-percentage')], className="text-primary"),
                ])
            ], className="shadow-sm"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H6("Male", className="mb-0")),
                    dbc.CardBody([
                        html.P(["Occupation Type: ", html.Span(id='highest-male-employment-occupation')], className="mb-0 text-muted"),
                        html.P(["Percentage (%): ", html.Span(id='highest-male-employment-percentage')], className="text-primary"),
                    ])
                ], className="shadow-sm")
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H6("Female", className="mb-0")),
                    dbc.CardBody([
                        html.P(["Occupation Type: ", html.Span(id='highest-female-employment-occupation')], className="mb-0 text-muted"),
                        html.P(["Percentage (%): ", html.Span(id='highest-female-employment-percentage')], className="mb-0 text-primary"),
                    ])
                ], className="shadow-sm")
            ], md=6)
        ]),
        html.H5("Greatest % Change in Employment between 2021 and 2023"),
        dbc.Row(["For ", html.Span(id='selected-region')]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H6('Overall',className="mb-0")),
                    dbc.CardBody([
                        html.P(["Occupation Type: ", html.Span(id='highest-year-disparity-occuptation')], className="mb-0 text-muted"),
                        html.P(["Percentage Change: ", html.Span(id='highest-year-disparity-percentage')], className="text-primary"),
                        html.P(["Gender: ", html.Span(id='highest-year-disparity-gender')]),
                        html.P(["Region: ", html.Span(id='highest-year-disparity-region')])
                    ])
                ], className="shadow-sm")
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H6('Male',className="mb-0")),
                    dbc.CardBody([
                        html.P([f"Occupation Type: {highest_m_year_disparity_occupation}"], className="mb-0 text-muted"),
                        html.P([f"Region: {highest_m_year_disparity_region}"], className="mb-0 text-muted"),
                        html.P([f"Percentage Change: {highest_m_year_disparity_percentage}"], className="text-primary"),
                    ])
                ], className="shadow-sm")
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H6('Female',className="mb-0")),
                    dbc.CardBody([
                        html.P([f"Occupation Type: {highest_f_year_disparity_occupation}"], className="mb-0 text-muted"),
                        html.P([f"Region: {highest_f_year_disparity_region}"], className="mb-0 text-muted"),
                        html.P([f"Percentage Change: {highest_f_year_disparity_percentage}"], className="text-primary"),
                    ])
                ], className="shadow-sm")
            ], md=6),
        ]), 
        dbc.Row(["Overall"]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H6('Overall',className="mb-0")),
                    dbc.CardBody([
                        html.P([f"Occupation Type: {highest_overall_disparity_occupation}"], className="mb-0 text-muted"),
                        html.P([f"Gender: {highest_overall_disparity_gender}"], className="mb-0 text-muted"),
                        html.P([f"Region: {highest_overall_disparity_region}"], className="mb-0 text-muted"),
                        html.P([f"Percentage Change: {highest_overall_disparity_percentage}"], className="text-primary"),
                    ])
                ], className="shadow-sm")
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H6('Male',className="mb-0")),
                    dbc.CardBody([
                        html.P([f"Occupation Type: {highest_m_year_disparity_occupation}"], className="mb-0 text-muted"),
                        html.P([f"Region: {highest_m_year_disparity_region}"], className="mb-0 text-muted"),
                        html.P([f"Percentage Change: {highest_m_year_disparity_percentage}"], className="text-primary"),
                    ])
                ], className="shadow-sm")
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H6('Female',className="mb-0")),
                    dbc.CardBody([
                        html.P([f"Occupation Type: {highest_f_year_disparity_occupation}"], className="mb-0 text-muted"),
                        html.P([f"Region: {highest_f_year_disparity_region}"], className="mb-0 text-muted"),
                        html.P([f"Percentage Change: {highest_f_year_disparity_percentage}"], className="text-primary"),
                    ])
                ], className="shadow-sm")
            ], md=6),
        ])
    ])
])

summary_stats = dbc.Card([
    dcc.Tabs(id='summary-tabs', children=[
        dcc.Tab(label='Gender Disparity Statistics', children=[gender_disparity_stats]),
        dcc.Tab(label='Occupation Statistics', children=[occupation_stats]),
    ])
], className="shadow", id="summary-stats", style={"display": "none"})

data_attribution = html.Div(
    [
        dbc.Button("Dataset", id="open-offcanvas", n_clicks=0),
        dbc.Offcanvas(
            html.P(
                "The data used in this analysis is sourced from the Greater London Authority, under the Open Government Licence v2.0."
            ),

            id="dataset-offcanvas",
            scrollable=True,
            title="Dataset Attribution",
            is_open=False,
        ),
    ]
)