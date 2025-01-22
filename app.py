from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Variable that defines the meta tag for the viewport
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Variable that contains the external_stylesheet to use, in this case Bootstrap styling from dash bootstrap components (dbc)
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Pass the stylesheet and meta_tag variables to the Dash app constructor
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags)

region_checklist = html.Div(
    [
        dbc.Label("Select the region"),
        dbc.RadioItems(
            options=[
                {"label": "England", "value": "england"},
                {"label": "Wales", "value": "wales"}
            ],
            value=[],
            id="region-checklist",
        ),
    ]
)

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
                {"label": "1: managers, directors and senior officials", "value": "Type 1"},
                {"label": "2: professional occupations", "value": "Type 2"},
                {"label": "3: associate prof & tech occupations", "value": "Type 3"}, 
                {"label": "4: administrative and secretarial occupations", "value": "Type 4"},
                {"label": "5: skilled trades occupations", "value": "Type 5"},
                {"label": "6: caring, leisure and other service occupations", "value": "Type 6"},
                {"label": "7: sales and customer service occupations", "value": "Type 7"},
                {"label": "8: process, plant and machine operatives", "value": "Type 8"},
                {"label": "9: elementary occupations", "value": "Type 9"},
            ],
            value=[],
            id="occupation-checklist",
        ),
    ]
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Comparative Employment Analysis Tool'))
    ]),

    dbc.Row([
        dbc.Col(html.H2('Selection filters'))
    ]),

    dbc.Row([
        dbc.Col(region_checklist, width=3),
        dbc.Col(year_checklist, width={"size": 3, "offset": 1}),
        dbc.Col(occupation_checklist, width={"size": 3, "offset": 1})
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='graph-content'))
    ])
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    app.run(debug=True)