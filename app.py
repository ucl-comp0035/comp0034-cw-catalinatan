from dash import Dash, html, dcc, callback, Output, Input, State, callback_context
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate

# Create dataframe
data_path = Path(__file__).parent / 'data' / 'employment_prepared.xlsx'
df = pd.read_excel(data_path)

# Variable that defines the meta tag for the viewport
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Variable that contains the external_stylesheet to use, in this case Bootstrap styling from dash bootstrap components (dbc)
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Pass the stylesheet and meta_tag variables to the Dash app constructor
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags)

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

occupation_type_slider = html.Div([
    html.Div([
        dbc.Label("Select a occupation type"),
    ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '8px'}),
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

@callback(
    Output('occupation-type-slider', 'tooltip'),
    Input('occupation-type-slider', 'value')
)

def update_tooltip(value):
    return {
        "placement": "bottom",
        "always_visible": True,
        "template": f"{full_descriptions[value]}"
    }

clear_button = html.Button('Clear selections', id='clear-button', n_clicks=0)

@app.callback(
    [Output('region-dropdown', 'value'),
     Output('year-dropdown', 'value'),
     Output('occupation-type-slider', 'value')],
    Input('clear-button', 'n_clicks'),
    [State('region-dropdown', 'value'),
     State('year-dropdown', 'value'),
     State('occupation-type-slider', 'value')]
)

def manage_dropdowns(n_clicks, region_value, year_value, occupation_value):
    ctx = callback_context

    if not ctx.triggered:
        raise PreventUpdate
    
    if ctx.triggered[0]['prop_id'].split ('.')[0] == 'clear-button':
        return None, None, 1
    
    # Return current values if not cleared
    return region_value, year_value, occupation_value

app.layout = dbc.Container([
    dbc.NavbarSimple(
            brand="Comparative Employment Analysis Tool", color="#4292C3", dark=True
        ),

    dbc.Row([
        dbc.Col(html.P("Selection filters"),width=2),
        dbc.Col(region_dropdown, width=4),
        dbc.Col(year_dropdown, width=4),
        dbc.Col(clear_button, width=2)
    ]),

    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id='stacked-bar-chart'), body=True), width=6),
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

@callback(
    Output('stacked-bar-chart', 'figure'),
    Input('region-dropdown', 'value'),
    Input('year-dropdown', 'value'),
)

def update_bar_chart(selected_region, selected_year):
    if not selected_region or not selected_year:
        raise PreventUpdate

    df['Short Occupation Type'] = df['Occupation Type'].str.split(':').str[0]

    filtered_df = df[
        (df['Region'] == selected_region) &
        (df['Year'] == int(selected_year))
    ]

    fig = px.bar(
        filtered_df,
        x="Short Occupation Type",
        y="Percentage Employed (Relative to Total Employment in the Year)",
        color="Gender",
        barmode="stack",
        title=f"Employment Data for {selected_region} in {selected_year} by Gender",
        color_discrete_map={'Female': '#B1172C', 'Male': '#4292C3'},
        hover_data={'Occupation Type': True, 'Short Occupation Type': False, 'Gender': True, 'Percentage Employed (Relative to Total Employment in the Year)': True}
    )

    fig.update_layout(
        title=dict(
            x=0.5,  # Center the title horizontally
            y=0.95,  # Move the title higher vertically (default is around 0.9)
            xanchor='center',  # Anchor the title at its center
            yanchor='top'  # Anchor the title at its top
        ),
        xaxis_title='Occupation Type',
        yaxis_title='Percentage Employed (Relative to Total Employment in the Year)',
        yaxis=dict(
            title_font=dict(size=12)
        )
    )
    return fig

@callback(
    Output('pie-chart', 'figure'),
    Input('region-dropdown', 'value'),
    Input('year-dropdown', 'value'),
)
def update_pie_chart(selected_region, selected_year):
    if not selected_region or not selected_year:
        raise PreventUpdate
    
    filtered_df = df[
        (df['Region'] == selected_region) &
        (df['Year'] == int(selected_year))
    ]

    disparity_df = filtered_df.pivot_table(
        index=['Region', 'Year', 'Occupation Type'],
        columns='Gender',
        values='Percentage Employed (Relative to Total Employment in the Year)',
        fill_value=0
    ).reset_index()

    disparity_df['Total Employment'] = disparity_df['Male'] + disparity_df['Female']

    fig = px.pie(
        disparity_df,  # Use disparity_df instead of filtered_df
        names='Occupation Type',
        values='Total Employment',
        title=f"Employment Data for {selected_region} in {selected_year} by Occupation Type",
        color_discrete_sequence=px.colors.sequential.RdBu
    )

    fig.update_layout(
        title=dict(
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top'
        ),
        margin=dict(l=50, r=200, t=50, b=50),  # Increase right margin
    )
    return fig


@callback(
    Output("disparity-map", "figure"),
    Input("year-dropdown", "value"),
    Input("occupation-type-slider", "value"),
)

def update_map(selected_year, selected_occupation):
    if not selected_year or not selected_occupation:
        raise PreventUpdate
    
    occupation_prefix = f"{selected_occupation}:"
    filtered_df = df[
        (df["Year"] == int(selected_year))
        & (df["Occupation Type"].str.startswith(occupation_prefix))
    ]

    disparity_df = filtered_df.pivot_table(
        index=['Region', 'Year', 'Occupation Type', 'Latitude', 'Longitude'],
        columns='Gender',
        values='Percentage Employed (Relative to Total Employment in the Year)',
        fill_value=0
    ).reset_index()
        
    disparity_df['Disparity'] = disparity_df['Male'] - disparity_df['Female']
    disparity_df['Total Employment'] = disparity_df['Male'] + disparity_df['Female']
    disparity_df['Disparity'] = disparity_df['Disparity'].abs()
    
    region_colors = {
        "England": "#5F001C",
        "Wales": "#D5604C",
        "Scotland": "#4292C3",
        "Northern Ireland": "#92C6DE"
    }
    fig = px.scatter_geo(
        disparity_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Region",
        size="Disparity",
        hover_data={
            'Disparity': ':.2f',
            'Total Employment': ':.2f',
            'Male': ':.2f',
            'Female': ':.2f',
            'Latitude': False,
            'Longitude': False,
            'Region': False  # Clean up hover data
        },
        title=f"Employment Disparity Map for {selected_year} by Occupation Type",
        scope='europe',
        projection='natural earth',
        color="Region",
        color_discrete_map=region_colors,
        fitbounds="locations"  # Auto-zoom to data points
    ).update_geos(
        visible=True,  # Show base map
        resolution=50,  # Better detail for Europe
        showcountries=True,  # Display country borders
        countrycolor="lightgrey",
        lataxis_range=[49, 60.5],  # Adjusted for UK coverage
        lonaxis_range=[-10.5, 2],  # Includes all UK regions
        center=dict(lon=-2, lat=54.5),  # Better UK center point
        projection_scale=2.3  # Fine-tuned zoom level
    ).update_traces(
        marker=dict(
            sizemin=4,  # Ensure small values are visible
            sizemode='diameter',
            sizeref=0.15,  # Adjust bubble scaling
            line=dict(width=0.5, color='darkgrey')
        )
    )

    fig.update_layout(
        title=dict(
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top'
        )
    )
    return fig

@callback(
    Output("stacked-area-chart", "figure"),
    Input("region-dropdown", "value"),
)

def update_area_chart(selected_region):
    if not selected_region:
        raise PreventUpdate

    filtered_df = df[
        (df["Region"] == selected_region)
    ]

    disparity_df = filtered_df.pivot_table(
        index=['Region', 'Year', 'Occupation Type'],
        columns='Gender',
        values='Percentage Employed (Relative to Total Employment in the Year)',
        fill_value=0
    ).reset_index()

    disparity_df['Total Employment'] = disparity_df['Male'] + disparity_df['Female']

    fig = px.area(
        disparity_df,
        x="Year",
        y="Total Employment",
        color="Occupation Type",
        title=f"Employment Trends by Sector (Up to 2023) in {selected_region}",
        labels={"Employment": "Percentage Employed (Relative to Total Employment in the Year)"},
        color_discrete_sequence=px.colors.sequential.RdBu,
    )

    # Update layout for better readability
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Percentage Employed",
        legend_title="Occupation Type",
        title_x=0.5,
    )

    fig.update_xaxes(
        tickvals=[2021, 2022, 2023],  # Values to show on the x-axis
        ticktext=["2021", "2022", "2023"],  # Corresponding labels for those values
        title="Year"
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)