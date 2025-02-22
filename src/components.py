from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
from pathlib import Path
import dash_daq as daq

# Create dataframe
data_path = Path(__file__).parent.parent / 'data' / 'employment_prepared.xlsx'
df = pd.read_excel(data_path)

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
display_summary_button = daq.BooleanSwitch(id='display-summary-button', on=False)

summary_stats = dbc.Card([
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
], className="shadow", id="summary-stats", style={"display": "none"})