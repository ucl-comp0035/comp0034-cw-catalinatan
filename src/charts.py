import plotly.express as px


def create_bar_chart(filtered_df, selected_region, selected_year):
    """
    Create a stacked bar chart showing employment data by gender for a
    selected region and year.

    Parameters:
    filtered_df (DataFrame): The filtered DataFrame containing the data to
        be plotted.
    selected_region (str): The selected region for the chart.
    selected_year (int): The selected year for the chart.

    Returns:
    fig (Figure): The Plotly figure object for the bar chart.
    """
    fig = px.bar(
        filtered_df,
        x="Short Occupation Type",
        y="Percentage Employed (Relative to Total Employment in the Year)",
        color="Gender",
        barmode="stack",
        title=(
            f"Employment Data for {selected_region} in {selected_year} "
            "by Gender"
        ),
        color_discrete_map={'Female': '#B1172C', 'Male': '#4292C3'},
        hover_data={
            'Occupation Type': True,
            'Short Occupation Type': False,
            'Gender': True,
            'Percentage Employed (Relative to Total Employment in the Year)': True
        }
    )

    fig.update_layout(
        title=dict(
            x=0.5,  # Center the title horizontally
            y=0.95,  # Move the title higher vertically (default is around 0.9)
            xanchor='center',  # Anchor the title at its center
            yanchor='top'  # Anchor the title at its top
        ),
        xaxis_title='Occupation Type',
        yaxis_title=(
            'Percentage Employed (Relative to Total Employment in the Year)'
        ),
        yaxis=dict(
            title_font=dict(size=12)
        )
    )
    return fig


def create_pie_chart(disparity_df, selected_region, selected_year):
    """
    Create a pie chart showing employment data by occupation type
    for a selected region and year.

    Parameters:
    disparity_df (DataFrame): The DataFrame containing the disparity
        data to be plotted.
    selected_region (str): The selected region for the chart.
    selected_year (int): The selected year for the chart.

    Returns:
    fig (Figure): The Plotly figure object for the pie chart.
    """
    fig = px.pie(
        disparity_df,  # Use disparity_df instead of filtered_df
        names='Occupation Type',
        values='Total Employment',
        title=(
            f"Employment Data for {selected_region} in {selected_year} "
            "by Occupation Type"
        ),
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


def create_disparity_map(disparity_df, selected_year):
    """
    Create a geographic scatter plot showing employment disparity by region
    for a selected year.

    Parameters:
    disparity_df (DataFrame): The DataFrame containing the disparity data to
        be plotted.
    selected_year (int): The selected year for the chart.

    Returns:
    fig (Figure): The Plotly figure object for the disparity map.
    """
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
        title=(
            f"Gender Disparity Map in Employment for {selected_year}"
            "by Occupation Type"
        ),
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


def create_area_chart(disparity_df, selected_region):
    """
    Create a stacked area chart showing employment trends by sector for a
    selected region.

    Parameters:
    disparity_df (DataFrame): The DataFrame containing the disparity data to
        be plotted.
    selected_region (str): The selected region for the chart.

    Returns:
    fig (Figure): The Plotly figure object for the area chart.
    """
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
        ticktext=["2021", "2022", "2023"],  # Corresponding labels for years
        title="Year"
    )
    return fig
