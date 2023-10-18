import json
import get_data

from dash import Dash, dcc, html
import plotly.graph_objects as go

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import geopandas as gpd

import plotly.express as px
import pandas as pd

app = Dash(__name__)
colors = {
    'background': '#ffffff',
    'text': '#000000'
}

df = get_data.gdf_fires
with open("gz_2010_us_040_00_5m_1.json", 'r') as f:
    states = json.load(f)

fig = go.Figure(data=go.Choropleth(
    locations=df['state'],
    z=df['number of fires'],
    locationmode='USA-states',
    colorscale='Reds',
))

fig.update_layout(
    title_text='Number of fires per state',
    geo_scope='usa',
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    coloraxis_colorbar_x=0.5

)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Simple app for spatial data visualisation',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    dcc.Graph(
        id='fires-in-2023',
        figure=fig
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
               10: 'October'},
    )
])


@app.callback(
    Output('fires-in-2023', 'figure'),
    Input('month-slider', 'value')
)
def update_map(selected_month):
    filtered_df = df[df['month'] == selected_month]
    number_to_months = {6: 'June',
                        7: 'July',
                        8: 'August',
                        9: 'September',
                        10: 'October'}

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


if __name__ == '__main__':
    app.run(debug=True)
