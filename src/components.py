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
    highest_f_year_disparity_region,
    highest_overall_disparity_percentage,
    highest_overall_disparity_occupation,
    highest_overall_disparity_region,
    highest_overall_disparity_gender  
)

# Create dataframe
data_path = Path(__file__).parent.parent / 'data' / 'employment_prepared.xlsx'
df = pd.read_excel(data_path)

# Dropdowns for region, year and occupation
region_dropdown = dcc.Dropdown(
    options=['England', 'Wales', 'Scotland', 'Northern Ireland'],
    value=None,
    id='region-dropdown',
    placeholder='Select a region',
    className="custom-dropdown"
)

year_dropdown = dcc.Dropdown(
    options=['2021', '2022', '2023'],
    value=None,
    id='year-dropdown',
    placeholder='Select a year',
    className="custom-dropdown"
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
        dbc.Label("Occupation Types", id='occupation-type-label'),
        dbc.Tooltip("Slide to select an occupation type", target='occupation-type-label', placement='top')
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
clear_button = html.Button('Clear', className="custom-button", id='clear-button', n_clicks=0)
clear_button_tooltip = dbc.Tooltip(
        "Clear all filters",  # Tooltip text
        target="clear-button",  # Connects to the button ID
        placement="bottom",  # Adjust as needed (top, bottom, left, right)
        className="custom-tooltip"  # Custom CSS class for styling
        )

# Save filters button 
save_filters_button = html.Button('Save', className="custom-button", id='save-filters-button', n_clicks=0)
save_filters_tooltip = dbc.Tooltip(
        "Save the current filters",  # Tooltip text
        target="save-filters-button",  # Connects to the button ID
        placement="bottom",  # Adjust as needed (top, bottom, left, right)
        className="custom-tooltip"  # Custom CSS class for styling
        )
save_filters_alert_message = dbc.Alert(
    id="save-alert",
    color="danger",
    dismissable=True,
    is_open=False,
)

analysis_name_input = dbc.InputGroup(
    [dbc.InputGroupText("Save analysis as"), dbc.Input(placeholder="Enter name", id="analysis-name-input")],
    className="custom-input-group")

# Display summary statistics button
display_summary_button = html.Button('Summary Statistics', className="custom-button", id='display-summary-button', n_clicks=0, style={"display": "none", "width": "100%"})
display_summary_tooltip = dbc.Tooltip(
        "Summarise gender and occupation statistics",  # Tooltip text
        target="display-summary-button",  # Connects to the button ID
        placement="top",  # Adjust as needed (top, bottom, left, right)
        className="custom-tooltip"  # Custom CSS class for styling
        )


def get_metric_style(value):
    """Return color and icon based on value positivity"""
    if value >= 0:
        return {"color": "success", "icon": "bi-arrow-up"}
    return {"color": "danger", "icon": "bi-arrow-down"}

# Summmary Gender Disparity Statistics
gender_disparity_stats = dbc.Card(
    [
        dbc.CardHeader(
            html.H4([
                html.I(className="bi bi-gender-female me-2"),
                html.I(className="bi bi-gender-male me-2"),
                "Gender Disparity Analysis"
            ], className="text-center text-white"),
            className="custom-stats-border"
        ),
        dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.H5(["Greatest Overall Disparity for ", html.Span(id='selected-occupation-type')], className="mb-0"),
                            className="bg-light"
                        ),
                        dbc.CardBody([
                            html.Div([
                                html.I(className="bi bi-geo-alt-fill text-muted me-2"),
                                html.Span("Region:", className="text-muted"),
                                html.Span(id='highest-disparity-region', className="h5 ms-2")
                            ], className="d-flex align-items-center mb-3"),
                            html.Div([
                                html.I(className="bi bi-bar-chart-line-fill me-2"),
                                html.Span("Disparity:", className="text-muted"),
                                html.Span(id='highest-disparity-percentage', className="h2 ms-2")
                            ], className="d-flex align-items-center")
                        ], className="border-start border-danger border-4 p-3")
                    ], className="shadow-lg h-100"),
                    md=6
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.H5(["Occupation Breakdown for ", html.Span(id='gen-selected-region'), " in ", html.Span(id='gen-selected-year')], className="mb-0"),
                            className="bg-light"
                        ),
                        dbc.CardBody([
                            html.Div([
                                html.I(className="bi bi-briefcase text-muted me-2"),
                                html.Span("Occupation:", className="text-muted"),
                                html.Span(id='highest-disparity-occupation', className="h5 ms-2")
                            ], className="d-flex align-items-center mb-3"),
                            html.Div([
                                html.I(className="bi bi-percent text-muted me-2"),
                                html.Span("Disparity:", className="text-muted"),
                                html.Span(id='highest-disparity-occupation-percentage', className="h2 ms-2")
                            ], className="d-flex align-items-center")
                        ], className="custom-male-border")
                    ], className="shadow-lg h-100"),
                    md=6
                )
            ], className="g-4")
        ], className="p-4")
    ],
    className="my-4 shadow-lg"
)

occupation_stats = dbc.Card(
    [
        dbc.CardHeader(
            html.H4(
                [
                    html.I(className="bi bi-briefcase me-2"), 
                    "Occupation Statistics"
                ],
                className="text-center text-white"
            ),
            className="custom-stats-border"
        ),
        dbc.CardBody([
            # Employment Change Section
            html.H5(
                [
                    html.I(className="bi bi-activity me-2"),
                    "Greatest % Change in Employment (2021-2023)"
                ],
                className="custom-header-style"
            ), 
            dbc.Row([
                # Overall Change Card
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.H6([
                                html.I(className="bi bi-globe me-2"),
                                'Overall'
                            ], className="mb-0 text-white"),
                            className="bg-warning"
                        ),
                        dbc.CardBody([
                            html.Div([
                                html.I(className="bi bi-briefcase me-2 text-muted"),
                                html.Span(f"Occupation: {highest_overall_disparity_occupation}", className="text-muted")
                            ], className="d-flex align-items-center mb-2"),
                            html.Div([
                                html.I(className="bi bi-gender-ambiguous me-2 text-muted"),
                                html.Span(f"Gender: {highest_overall_disparity_gender}")
                            ], className="d-flex align-items-center mb-2"),
                            html.Div([
                                html.I(className="bi bi-geo me-2 text-muted"),
                                html.Span(f"Region: {highest_overall_disparity_region}")
                            ], className="d-flex align-items-center"),
                            html.Div([
                                html.I(className=f"bi {get_metric_style(float(highest_overall_disparity_percentage))['icon']} me-2"),
                                html.Span(f"{highest_overall_disparity_percentage}%", 
                                        className=f"h4 text-{get_metric_style(float(highest_overall_disparity_percentage))['color']}")
                            ], className="d-flex align-items-center mb-2"),
                        ], className="border-start border-purple border-4 p-3")
                    ], className="shadow-lg h-100"),
                    md=4
                ),
                
                # Male Change Card
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.H6([
                                html.I(className="bi bi-gender-male me-2"),
                                'Male'
                            ], className="mb-0 text-white"),
                            style={"backgroundColor": "#4291C3"}
                        ),
                        dbc.CardBody([
                            html.Div([
                                html.I(className="bi bi-briefcase me-2 text-muted"),
                                html.Span(f"Occupation: {highest_m_year_disparity_occupation}", className="text-muted")
                            ], className="d-flex align-items-center mb-2"),
                            html.Div([
                                html.I(className="bi bi-geo me-2 text-muted"),
                                html.Span(f"Region: {highest_m_year_disparity_region}", className="text-muted")
                            ], className="d-flex align-items-center mb-2"),
                            html.Div([
                                html.I(className=f"bi {get_metric_style(float(highest_m_year_disparity_percentage))['icon']} me-2"),
                                html.Span(f"{highest_m_year_disparity_percentage}%", 
                                        className=f"h4 text-{get_metric_style(float(highest_m_year_disparity_percentage))['color']}")
                            ], className="d-flex align-items-center")
                        ], className="custom-male-border")
                    ], className="shadow-lg h-100", style={"marginBottom": "15px"}),
                    md=4
                ),
                
                # Female Change Card
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.H6([
                                html.I(className="bi bi-gender-female me-2"),
                                'Female'
                            ], className="mb-0 text-white"),
                            style={"backgroundColor": "#D6604D"}
                        ),
                        dbc.CardBody([
                            html.Div([
                                html.I(className="bi bi-briefcase me-2 text-muted"),
                                html.Span(f"Occupation: {highest_f_year_disparity_occupation}", className="text-muted")
                            ], className="d-flex align-items-center mb-2"),
                            html.Div([
                                html.I(className="bi bi-geo me-2 text-muted"),
                                html.Span(f"Region: {highest_f_year_disparity_region}", className="text-muted")
                            ], className="d-flex align-items-center mb-2"),
                            html.Div([
                                html.I(className=f"bi {get_metric_style(float(highest_f_year_disparity_percentage))['icon']} me-2"),
                                html.Span(f"{highest_f_year_disparity_percentage}%", 
                                        className=f"h4 text-{get_metric_style(float(highest_f_year_disparity_percentage))['color']}")
                            ], className="d-flex align-items-center")
                        ], className="custom-female-border")
                    ], className="shadow-lg h-100"),
                    md=4
                )
            ], className="g-4", style={"marginBottom": "15px"}),

            html.Div(
                [
                    html.I(className="bi bi-geo-alt me-2"),
                    html.P(["For ",
                    html.Span(id='occ-selected-region', className="fw-bold"),
                    " in ",
                    html.Span(id='occ-selected-year', className="fw-bold")])
                ],
                className="custom-location-header-style"
            ),
            
            # Highest Employment Section
            html.H5(
                [
                    html.I(className="bi bi-trophy me-2"),
                    "Highest Employment Percentage (%)"
                ],
                className="custom-header-style"
            ),
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.H6(
                                [
                                    html.I(className="bi bi-star-fill me-2"),
                                    "Overall"
                                ],
                                className="mb-0 text-white"
                            ),
                            className="bg-warning"
                        ),
                        dbc.CardBody([
                            html.Div(
                                [
                                    html.I(className="bi bi-briefcase me-2 text-muted"),
                                    html.Span(id='highest-employment-occupation', className="h6")
                                ],
                                className="d-flex align-items-center mb-3"
                            ),
                            html.Div(
                                [
                                    html.I(className="bi bi-percent me-2 text-warning"),
                                    html.Span(id='highest-employment-percentage', className="h2 fw-bold")
                                ],
                                className="d-flex align-items-center"
                            )
                        ], className="border-start border-warning border-4")
                    ], className="shadow-lg h-100"),
                    md=4
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.H6(
                                [
                                    html.I(className="bi bi-gender-male me-2"),
                                    "Male"
                                ],
                                className="mb-0 text-white"
                            ),
                            style={"backgroundColor": "#4291C3"}
                        ),
                        dbc.CardBody([
                            html.P(
                                [
                                    html.I(className="bi bi-briefcase me-2 text-muted"),
                                    html.Span(id='highest-male-employment-occupation')
                                ],
                                className="text-truncate mb-2"
                            ),
                            html.Div(
                                [
                                    html.I(className="bi bi-percent text-success"),
                                    html.Span(id='highest-male-employment-percentage', className="h4 text-success ms-2")
                                ],
                                className="d-flex align-items-center"
                            )
                        ], className="custom-male-border")
                    ], className="shadow-sm h-100"),
                    md=4
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.H6(
                                [
                                    html.I(className="bi bi-gender-female me-2"),
                                    "Female"
                                ],
                                className="mb-0 text-white"
                            ),
                            style={"backgroundColor": "#D6604D"},
                        ),
                        dbc.CardBody([
                            html.P(
                                [
                                    html.I(className="bi bi-briefcase me-2 text-muted"),
                                    html.Span(id='highest-female-employment-occupation')
                                ],
                                className="text-truncate mb-2"
                            ),
                            html.Div(
                                [
                                    html.I(className="bi bi-percent text-success"),
                                    html.Span(id='highest-female-employment-percentage', className="h4 text-success ms-2")
                                ],
                                className="d-flex align-items-center"
                            )
                        ], className="custom-female-border")
                    ], className="shadow-sm h-100"),
                    md=4
                )
            ], className="g-4 mb-5"),
        ], className="p-4")
    ],
    className="my-4 shadow-lg"
)

summary_stats = html.Div([
    display_summary_button,
    display_summary_tooltip,
    dbc.Collapse(
        dcc.Tabs(
            children=[
                dcc.Tab(label='Gender Disparity Statistics', children=[gender_disparity_stats]),
                dcc.Tab(label='Occupation Statistics', children=[occupation_stats]),
            ],
            className="tab-container",
            parent_className="custom-tabs",
            parent_style={"margin": "0"},
        ),
        id="summary-stats",
        is_open=False
    ),
    dcc.Download(id="export-stats")
], className="shadow tab-content")

data_attribution = html.Div(
    [
        dbc.Button("Dataset", id="data-attribution-button", className="custom-button", n_clicks=0),
        dbc.Tooltip(
            "View dataset attribution",  # Tooltip text
            id="dataset-tooltip",
            target="data-attribution-button",  # Connects to the button ID
            placement="bottom",  # Adjust as needed (top, bottom, left, right)
            className="custom-tooltip"  # Custom CSS class for styling,
        ),
        dbc.Offcanvas(
            children=[
                html.Div([
                    html.P(
                        "The data used in this analysis is sourced from the Greater London Authority, under the Open Government Licence v2.0."
                    ),
                    html.P([
                        "Please refer to ",
                        html.A("this website", href="https://data.london.gov.uk/dataset/employment-occupation-type-and-gender-borough", target="_blank"),
                        " for more information."
                    ]),
                ]),
            ],
            id="data-attribution-canvas",
            scrollable=True,
            title="Dataset Attribution",
            is_open=False,
        ),
    ]
)