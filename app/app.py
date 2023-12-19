import json
import pandas as pd

import plotly.graph_objects as go

from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import statistics

df = pd.read_csv('df.csv')
with open("gz_2010_us_040_00_5m_1.json", 'r') as f:
    states = json.load(f)

number_to_months = {6: 'June',
                    7: 'July',
                    8: 'August',
                    9: 'September',
                    10: 'October'}

external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__, external_stylesheets=external_stylesheets)
colors = {
    'background': '##ebeced',
    'text': '#000000'
}

text = str('Burnt area in [km') + '\u00B2' + str(']')

app.layout = dbc.Container([

    dbc.Row([
        html.H1('\n'),
        html.H1('\n'),
        html.H1('\n'),
        html.H1('\n')
    ]),

    dbc.Row([
        dbc.Col([
            html.H3("Wildfires in the USA",
                    className='text-center text-primary mb-4'),
            html.H5(
                "Below you can see a simple app for spatial data visualization. Choose options below to see desired "
                "data."),

            html.H6("Choose month to see the median:"),
            dcc.Checklist(
                id='my_checklist',
                options=[
                    {'label': x, 'value': x, 'disabled': False}
                    for x in df['month_name'].unique()
                ],
                value=['October'],
                inline=True,
                labelStyle={"display": "flex", "align-items": "center"}

            ),
            html.H4(id='median-months'),

        ], width=2, style={'backgroundColor': 'rgb(237, 238, 240)'}),

        dbc.Col([
            dbc.Row([
                html.H5(
                    children='Choose month to see the data on both map and bar graph:',
                    style={'margin-top': '50px'}

                ),

                dcc.Slider(
                    df['month'].min(),
                    df['month'].max(),
                    step=None,
                    id='month-slider',
                    value=df['month'].max(),
                    marks={6: 'June',
                           7: 'July',
                           8: 'August',
                           9: 'September',
                           10: 'October'}
                ),
                dbc.Col([
                    dcc.Graph(
                        id='fires-in-2023',
                        figure={},
                    ),
                ], width=7),

                dbc.Col([
                    html.H5(
                        children='Choose type of data presented on the bar graph:'

                    ),
                    dcc.Dropdown(id='bardropdown',
                                 options=[
                                     {'label': 'Burnt area in [%]', 'value': 'burnt area [%]'},
                                     {'label': text, 'value': 'burnt area [km2]'},
                                 ],
                                 value='burnt area [km2]',
                                 multi=False,
                                 clearable=False
                                 ),
                    dcc.Graph(
                        id='bar-graph',
                        figure={},

                    ),

                ], width=5),
            ]),
        ])

    ]),
])


@app.callback(
    Output('fires-in-2023', 'figure'),
    Input('month-slider', 'value')
)
def update_map(selected_month):
    """
    Callback to update the map based on the selected month.

    Parameters:
    selected_month (int): Selected month.

    Returns:
    go.Figure: Updated map figure.
    """
    filtered_df = df[df['month'] == selected_month]
    # number_to_months = {6: 'June',
    #                     7: 'July',
    #                     8: 'August',
    #                     9: 'September',
    #                     10: 'October'}

    month_name = number_to_months.get(selected_month)

    fig = go.Figure(data=go.Choropleth(
        locations=filtered_df['state'],
        z=filtered_df['number of fires'],
        zmin=0,
        zmax=28,
        locationmode='USA-states',
        colorscale='Reds',
    ))

    fig.update_layout(
        title_text=f'Number of fires per state in {month_name}',
        geo_scope='usa',
    )

    return fig


@app.callback(
    Output('bar-graph', 'figure'),
    [Input('month-slider', 'value'),
     Input('bardropdown', 'value')]
)
def update_bar_graph(selected_month, bardropdown):
    """
    Callback to update the bar graph based on the selected month and data type.

    Parameters:
    - selected_month (int): Selected month.
    - bardropdown (str): Selected data type.

    Returns:
    px.bar: Updated bar graph figure.
    """
    filtered_df = df[df['month'] == selected_month]

    month_name = number_to_months.get(selected_month)
    fig = px.bar(data_frame=filtered_df,
                 x='state',
                 y=bardropdown,
                 title=f'Burnt area per state in {month_name}'
                 )

    fig.update_traces(marker_color='darkred',
                      marker_line_width=2, opacity=1)

    return fig


@app.callback(
    Output('median-months', 'children'),
    Input('my_checklist', 'value')
)
def median_months(checked_options):
    """
    Callback to calculate and display the median based on the selected months.

    Parameters:
    checked_options (list): List of selected months.

    Returns:
    str: Displayed median information.
    """
    filtered_df = df[df['month_name'].isin(checked_options)]
    if not checked_options:
        return "Median is: 0"
    else:
        return f"Median is: ", statistics.median(filtered_df['number of fires'])


if __name__ == '__main__':
    app.run(debug=True)
