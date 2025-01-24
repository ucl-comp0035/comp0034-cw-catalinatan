from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate

# Create dataframe
df = pd.read_excel('data/employment_prepared.xlsx')

# Variable that defines the meta tag for the viewport
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Variable that contains the external_stylesheet to use, in this case Bootstrap styling from dash bootstrap components (dbc)
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Pass the stylesheet and meta_tag variables to the Dash app constructor
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags)

# Implement drop down later with radio items with clicks 
region_checklist = dbc.Card([
    dbc.CardBody([html.Div(
    [
        dbc.Label("Select the region", style={"fontWeight": "bold"}),
        dbc.RadioItems(
            options=[
                {"label": "England", "value": "England"},
                {"label": "Wales", "value": "Wales"}
            ],
            value=[],
            id="region-checklist",
        ),
    ]
    ),
    ])
],color='light')

year_checklist = html.Div(
    [
        dbc.Label("Select the year"),
        dbc.RadioItems(
            options=[
                {"label": "2021", "value": "2021"},
                {"label": "2022", "value": "2022"},
                {"label": "2023", "value": "2023"}
            ],
            value=[],
            id="year-checklist",
        ),
    ]
)

occupation_checklist = html.Div(
    [
        dbc.Label("Select the occupation type"),
        dbc.Checklist(
            options=[
                {"label": "1: managers, directors and senior officials", "value": "1: managers, directors and senior officials"},
                {"label": "2: professional occupations", "value": "2: professional occupations"},
                {"label": "3: associate prof & tech occupations", "value": "3: associate prof & tech occupations"}, 
                {"label": "4: administrative and secretarial occupations", "value": "4: administrative and secretarial occupations"},
                {"label": "5: skilled trades occupations", "value": "5: skilled trades occupations"},
                {"label": "6: caring, leisure and other service occupations", "value": "6: caring, leisure and other service occupations"},
                {"label": "7: sales and customer service occupations", "value": "7: sales and customer service occupations"},
                {"label": "8: process, plant and machine operatives", "value": "8: process, plant and machine operatives"},
                {"label": "9: elementary occupations", "value": "9: elementary occupations"},
            ],
            value=[],
            id="occupation-checklist",
        ),
    ]
)

app.layout = dbc.Container([
    dbc.NavbarSimple(brand="Comparative Employment Analysis Tool", 
                     color="primary", 
                     dark=True
    ),

    dbc.Row([
        dbc.Col(html.H2('Selection filters'))
    ]),

    dbc.Row([
        dbc.Col(region_checklist, width=3),
        dbc.Col(year_checklist, width={"size": 3, "offset": 1}),
        dbc.Col(occupation_checklist, width={"size": 3, "offset": 1})
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='stacked-bar-chart'))
    ])
])

@callback(
    Output('stacked-bar-chart', 'figure'),
    Input('region-checklist', 'value'),
    Input('year-checklist', 'value'),
    Input('occupation-checklist', 'value')
)

def update_graph(selected_region, selected_year, selected_occupations):
    if not selected_region or not selected_year or not selected_occupations:
        raise PreventUpdate

    filtered_df = df[
        (df['Region'] == selected_region) &
        (df['Year'] == int(selected_year)) &
        (df['Occupation Type'].isin(selected_occupations))
    ]

    fig1 = px.bar(
        filtered_df,
        x='Occupation Type',
        y='Percentage Employed (Relative to Total Employment in the Year)',
        color='Gender',
        barmode='stack',
        title='Employment Data for {} in {}'.format(selected_region, selected_year),
    )

    # fig2 = px.scatter(
    #     filtered_df,

    # )
    return fig1

if __name__ == '__main__':
    app.run(debug=True)