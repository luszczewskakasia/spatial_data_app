import json

from dash import Dash, dcc, html
import plotly.graph_objects as go
import geopandas as gpd

import plotly.express as px
import pandas as pd


app = Dash(__name__)
colors = {
    'background': '#ffffff',
    'text': '#000000'
}

df = pd.read_csv('df.csv')
with open("gz_2010_us_040_00_5m_1.json", 'r') as f:
    states = json.load(f)

fig = go.Figure(data=go.Choropleth(
    locations=df['STATE ID'],
    z=df['FIRE'],
    locationmode='USA-states',
    colorscale='Reds',
))

fig.update_layout(
    title_text='Number of fires per state',
    geo_scope='usa',
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
    # it'll work, when I add years
    # dcc.Slider(
    # gdf['month'].min(),
    # gdf['month'].max(),
    # step=None,
    # id='year--slider',
    # value=gdf['month'].max(),
    # marks={str(year): str(year) for year in gdf['month'].unique()},
    # )
])

if __name__ == '__main__':
    app.run(debug=True)