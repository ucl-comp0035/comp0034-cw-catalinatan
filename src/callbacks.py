from dash import Output, Input, State, callback_context, html, dcc, no_update
from dash.dependencies import ALL, MATCH  # Add MATCH import
from dash.exceptions import PreventUpdate
from components import full_descriptions, df
import dash_bootstrap_components as dbc
from charts import (
    create_bar_chart,
    create_pie_chart,
    create_disparity_map,
    create_area_chart
)
from filter_data_functions import filter_dataframe, prepare_disparity_df# Ensure prepare_year_disparity_df is imported
import json

def clear_analysis_name(n_clicks):
    """
    Clear the analysis name input field when the save button is clicked.
    """
    if n_clicks:
        return ""
    return no_update


def save_filters(n_clicks, custom_analysis_name, region, year, occupation, current_data, current_menu_items):
    if not n_clicks:
        raise PreventUpdate

    if not region or not year:
        return no_update, no_update, True, "Please select a region and year before saving an analysis."

    # Ensure the input has a valid name
    analysis_name = custom_analysis_name.strip() if custom_analysis_name else f"Analysis {len(current_data) + 1}: {region}, {year}"

    # Check if the analysis name already exists
    if any(analysis["name"] == analysis_name for analysis in current_data):
        return no_update, no_update, True, f"An analysis named '{analysis_name}' already exists. Please choose a different name."

    # Append new analysis
    new_analysis = {
        "name": analysis_name,
        "region": region,
        "year": year,
        "occupation": occupation
    }

    updated_data = current_data + [new_analysis] if current_data else [new_analysis]

    new_menu_item = dbc.DropdownMenuItem(
        analysis_name,
        id={"type": "saved-analysis", "index": len(updated_data) - 1},
        n_clicks=0
    )

    updated_menu_items = current_menu_items + [new_menu_item] if current_menu_items else [new_menu_item]

    return updated_menu_items, updated_data, False, no_update

def update_tooltip(value):
    """
    Update the tooltip for the occupation type slider.
    """
    return {
        "placement": "bottom",
        "always_visible": True,
        "template": f"{full_descriptions[value]}"
    }
        

def update_selected_filters_for_gender_stats(selected_region, selected_year):
    """
    Update the selected region, year and occupation based on the selected
    values.
    """

    if not selected_region or not selected_year:
        raise PreventUpdate

    return selected_region, selected_year

def update_selected_filters_for_occ_stats(selected_region, selected_year, selected_occupation):
    """
    Update the selected region, year and occupation based on the selected
    values.
    """

    if not selected_region or not selected_year or not selected_occupation:
        raise PreventUpdate

    return selected_region, selected_year, full_descriptions[selected_occupation]

def update_highest_disparity_region(selected_occupation, selected_year):
    """
    Update the highest disparity region based on the selected occupation
    and year.
    """
    if not selected_occupation or not selected_year:
        raise PreventUpdate

    occupation_prefix = f"{selected_occupation}:"
    filtered_df = filter_dataframe(
        year=selected_year, occupation_prefix=occupation_prefix
    )
    disparity_df = prepare_disparity_df(filtered_df)

    highest_disparity_percentage = disparity_df['Disparity'].max()
    highest_disparity_perc_idx = disparity_df['Disparity'].idxmax()
    highest_disparity_region = disparity_df['Region'][highest_disparity_perc_idx]

    return highest_disparity_region, f"{highest_disparity_percentage:.2f}%"

def update_highest_disparity_occupation_for_selected_region(selected_region, selected_year):
    """
    Update the highest disparity occupation based on the selected region
    and year.
    """
    if not selected_region or not selected_year:
        raise PreventUpdate

    filtered_df = filter_dataframe(region=selected_region, year=selected_year)
    disparity_df = prepare_disparity_df(filtered_df)

    highest_disparity_percentage = disparity_df['Disparity'].max()
    highest_disparity_perc_idx = disparity_df['Disparity'].idxmax()
    highest_disparity_occupation = disparity_df['Occupation Type'][highest_disparity_perc_idx]

    return highest_disparity_occupation, f"{highest_disparity_percentage:.2f}%"

def update_highest_male_employment_occupation(selected_region, selected_year):
    """
    Update the highest male employment occupation based on the selected region
    and year.
    """
    if not selected_region or not selected_year:
        raise PreventUpdate
    
    male_df = filter_dataframe(region=selected_region, year=selected_year, gender='Male')

    highest_male_employment_percentage = male_df['Percentage Employed (Relative to Total Employment in the Year)'].max()
    highest_male_employ_perc_idx = male_df['Percentage Employed (Relative to Total Employment in the Year)'].idxmax()
    highest_male_employment_occupation = male_df['Occupation Type'][highest_male_employ_perc_idx]

    return highest_male_employment_occupation, f"{highest_male_employment_percentage:.2f}%"

def update_highest_female_employment_occupation(selected_region, selected_year):
    """
    Update the highest female employment occupation based on the selected region
    and year.
    """
    if not selected_region or not selected_year:
        raise PreventUpdate
    
    female_df = filter_dataframe(region=selected_region, year=selected_year, gender='Female')

    highest_female_employment_percentage = female_df['Percentage Employed (Relative to Total Employment in the Year)'].max()
    highest_female_employ_perc_idx = female_df['Percentage Employed (Relative to Total Employment in the Year)'].idxmax()
    highest_female_employment_occupation = female_df['Occupation Type'][highest_female_employ_perc_idx]

    return highest_female_employment_occupation, f"{highest_female_employment_percentage:.2f}%"

def update_highest_overall_employment_occupation(selected_region, selected_year):
    """
    Update the highest overall employment occupation based on the selected region
    and year.
    """
    if not selected_region or not selected_year:
        raise PreventUpdate
    
    filtered_df = filter_dataframe(region=selected_region, year=selected_year)
    disparity_df = prepare_disparity_df(filtered_df)
    highest_employment_percentage = disparity_df['Total Employment'].max()
    highest_employ_perc_idx = disparity_df['Total Employment'].idxmax()
    highest_employment_occupation = disparity_df['Occupation Type'][highest_employ_perc_idx]

    return highest_employment_occupation, f"{highest_employment_percentage:.2f}%"

def show_summary_button(selected_region, selected_year, selected_occupation):
    if not selected_region or not selected_year or not selected_occupation:
        return {'display': 'none', "width": "100%"}
    return {'display': 'block', "width": "100%"}

def toggle_data_attribution(n_clicks, is_open):
    """
    Toggle the display of data attribution based on the button click.
    """
    if n_clicks:
        return not is_open
    return is_open

def register_callbacks(app):
    """
    Register all callbacks for the Dash app.
    """
    @app.callback(
        Output("analysis-name-input", "value"),
        Input("save-filters-button","n_clicks"),
    )
    
    def wrapped_clear_analysis_name(n_clicks):
        return clear_analysis_name(n_clicks)
    
    @app.callback(
        Output("saved-analyses-menu", "children"),
        Output("saved-analyses-store", "data"),
        Output("save-alert", "is_open"),
        Output("save-alert", "children"),
        Input("save-filters-button", "n_clicks"),
        State("analysis-name-input", "value"),
        State("region-dropdown", "value"),
        State("year-dropdown", "value"),
        State("occupation-type-slider", "value"),
        State("saved-analyses-store", "data"),
        State("saved-analyses-menu", "children"),
        prevent_initial_call=True
    )
    
    def wrapped_save_filters(n_clicks, custom_analysis_name, region, year, occupation, current_data, current_menu_items):
        return save_filters(n_clicks, custom_analysis_name, region, year, occupation, current_data, current_menu_items)

    @app.callback(
        [
            Output("region-dropdown", "value"),
            Output("year-dropdown", "value"),
            Output("occupation-type-slider", "value"),
            Output("summary-stats", "is_open")
        ],
        [
            Input({"type": "saved-analysis", "index": ALL}, "n_clicks"),
            Input('clear-button', 'n_clicks'),
            Input('display-summary-button', 'n_clicks')
        ],
        [
            State("saved-analyses-store", "data"),
            State('region-dropdown', 'value'),
            State('year-dropdown', 'value'),
            State('occupation-type-slider', 'value'),
            State('summary-stats', 'is_open')
        ],
        prevent_initial_call=True,
    )
    def manage_dropdowns(saved_n_clicks, clear_n_clicks, summary_n_clicks, data, region_value, year_value, occupation_value, summary_status):
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'clear-button':
            return None, None, 1, False

        if triggered_id == 'display-summary-button':
            return region_value, year_value, occupation_value, not summary_status

        try:
            triggered_id = json.loads(triggered_id)
            if triggered_id.get("type") == "saved-analysis":
                analysis_index = triggered_id["index"]
                if 0 <= analysis_index < len(data):
                    analysis_data = data[analysis_index]
                    return analysis_data["region"], analysis_data["year"], analysis_data["occupation"], summary_status
        except json.JSONDecodeError:
            pass

        return region_value, year_value, occupation_value, summary_status

    
    @app.callback(
        Output('display-summary-button','style'),
        Input('region-dropdown','value'),
        Input('year-dropdown','value'),
        Input('occupation-type-slider','value')
    )

    def show_summary_button(selected_region, selected_year, selected_occupation):
        if not selected_region or not selected_year or not selected_occupation:
            return {'display': 'none', "width": "100%"}
        return {'display': 'block', "width": "100%"}

    @app.callback(
        Output('occupation-type-slider', 'tooltip'),
        Input('occupation-type-slider', 'value')
    )
    
    def wrapped_update_tooltip(value):
        return update_tooltip(value)
    
    @app.callback(
        Output('bar-chart-card-content', 'children'),
        Input('region-dropdown', 'value'),
        Input('year-dropdown', 'value'),
    )
    
    def update_bar_chart(selected_region, selected_year):
        """
        Update the stacked bar chart based on the selected region and year.
        """
        if not selected_region or not selected_year:
        # Return a figure with only the placeholder image
            return html.Div([
                html.I(className="custom-icon bi bi-lock"),
                html.Img(src=app.get_asset_url('stacked_bar_chart.png'), className='custom-placeholder')
                ])
        else: 
            filtered_df = filter_dataframe(
                region=selected_region, year=selected_year)
            filtered_df['Short Occupation Type'] = filtered_df['Occupation Type'] \
                .str.split(':').str[0]
            # Call your function to create the bar chart
            bar_chart_figure = create_bar_chart(filtered_df, selected_region, selected_year)

            return dcc.Graph(figure=bar_chart_figure)
    
    @app.callback(
        Output('pie-chart-card-content', 'children'),
        Input('region-dropdown', 'value'),
        Input('year-dropdown', 'value'),
    )
    
    def update_pie_chart(selected_region, selected_year):
        """
        Update the pie chart based on the selected region and year.
        """
        if not selected_region or not selected_year:
            return html.Div([
                html.I(className="custom-icon bi bi-lock"),
                html.Img(src=app.get_asset_url('pie_chart_placeholder.png'), className='custom-placeholder')
                ])
        else:
            filtered_df = filter_dataframe(
                region=selected_region, year=selected_year)
            disparity_df = prepare_disparity_df(filtered_df)
            pie_chart_figure = create_pie_chart(disparity_df, selected_region, selected_year)
            return dcc.Graph(figure=pie_chart_figure)
    
    @app.callback(
        Output("disparity-map-card-content", "children"),
        Input("year-dropdown", "value"),
        Input("occupation-type-slider", "value"),
    )
    
    def update_map(selected_year, selected_occupation):
        """
        Update the disparity map based on the selected year and occupation
        type.
        """
        if not selected_year or not selected_year:
            return html.Div([
                html.I(className="custom-icon bi bi-lock"),
                html.Img(src=app.get_asset_url('disparity_map_placeholder.png'), className='custom-placeholder')
                ])

        else:
            occupation_prefix = f"{selected_occupation}:"
            filtered_df = filter_dataframe(
                year=selected_year, occupation_prefix=occupation_prefix
            )
            disparity_df = prepare_disparity_df(filtered_df)
            disparity_map_figure = create_disparity_map(disparity_df, selected_year)
            return dcc.Graph(figure=disparity_map_figure)

    
    @app.callback(
        Output("stacked-area-chart-card-content", 'children'),
        Input("region-dropdown", 'value'),
    )
    
    def update_area_chart(selected_region):
        """
        Update the stacked area chart based on the selected region.
        """
        if not selected_region:
            return html.Div([
                html.I(className="custom-icon bi bi-lock"),
                html.Img(src=app.get_asset_url('stacked_area_chart_placeholder.png'), className='custom-placeholder')
                ])
        
        else:
            filtered_df = filter_dataframe(region=selected_region)
            disparity_df = prepare_disparity_df(filtered_df)
            area_chart_figure = create_area_chart(disparity_df, selected_region)
            return dcc.Graph(figure=area_chart_figure)
            
    @app.callback(
        Output("gen-selected-region", "children"),
        Output("gen-selected-year", "children"),
        Input("region-dropdown", "value"),
        Input("year-dropdown", "value"),
    )
    
    def wrapped_update_selected_filters_for_gender_stats(selected_region, selected_year):
        return update_selected_filters_for_gender_stats(selected_region, selected_year)
    
    @app.callback(
        Output("occ-selected-region", "children"),
        Output("occ-selected-year", "children"),
        Output('selected-occupation-type', 'children'),
        Input("region-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input('occupation-type-slider', 'value')
    )
    
    def wrapped_update_selected_filters_for_occ_stats(selected_region, selected_year, selected_occupation):
        return update_selected_filters_for_occ_stats(selected_region, selected_year, selected_occupation)
    
    @app.callback(
        Output("highest-disparity-region", "children"),
        Output("highest-disparity-percentage", "children"),
        Input("occupation-type-slider", "value"),
        Input("year-dropdown", "value"),
    )
    
    def wrapped_update_highest_disparity_region(selected_occupation, selected_year):
        return update_highest_disparity_region(selected_occupation, selected_year)
    
    @app.callback(
        Output("highest-disparity-occupation", "children"),
        Output("highest-disparity-occupation-percentage", "children"),
        Input("region-dropdown", "value"),
        Input("year-dropdown", "value"),
        allow_duplicate=True
    )
    def wrapped_update_highest_disparity_occupation_for_selected_region(selected_region, selected_year):
        return update_highest_disparity_occupation_for_selected_region(selected_region, selected_year)
    
    @app.callback(
        Output("highest-male-employment-occupation","children"),
        Output("highest-male-employment-percentage","children"),
        Input("region-dropdown","value"),
        Input("year-dropdown","value")
    )
    
    def wrapped_update_highest_male_employment_occupation(selected_region, selected_year):
        return update_highest_male_employment_occupation(selected_region, selected_year)

    @app.callback(
        Output("highest-female-employment-occupation","children"),
        Output("highest-female-employment-percentage","children"),
        Input("region-dropdown","value"),
        Input("year-dropdown","value")
    )
   
    def wrapped_update_highest_female_employment_occupation(selected_region, selected_year):
        return update_highest_female_employment_occupation(selected_region, selected_year)
    
    @app.callback(
        Output("highest-employment-occupation","children"),
        Output("highest-employment-percentage","children"),
        Input("region-dropdown","value"),
        Input("year-dropdown","value")
    )

    def wrapped_update_highest_overall_employment_occupation(selected_region, selected_year):
        return update_highest_overall_employment_occupation(selected_region, selected_year)

    @app.callback(
        Output("data-attribution-canvas","is_open"),
        Input("data-attribution-button","n_clicks"),
        State("data-attribution-canvas","is_open"),
        prevent_initial_call=True
    )

    def wrapped_toggle_data_attribution(n_clicks, is_open):
        return toggle_data_attribution(n_clicks, is_open)