import json
import get_data

from dash import Dash, dcc, html
import plotly.graph_objects as go

from dash import dcc, html
from dash.dependencies import Input, Output

import plotly.express as px

df = get_data.gdf_fires
with open("gz_2010_us_040_00_5m_1.json", 'r') as f:
    states = json.load(f)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
colors = {
    'background': '##ebeced',
    'text': '#000000'
}

app.layout = html.Div(
    children=[
        html.H3(
            className='banner',
            children='WILDFIRES IN the USA',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.Div([
            html.H5(
                className='six columns',
                children='Choose month to see the data on both map and bar graph:'
            ),

            html.H5(
                className='six columns',
                children='Choose type of data presented on the bar graph:'
            )
        ], className='row'),


        html.Div([
            html.Div([
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
            ], className='six columns'),

            html.Div([
                dcc.Dropdown(id='bardropdown',
                             options=[
                                 {'label': 'Burnt area in [%]', 'value': 'burnt area [%]'},
                                 {'label': 'Burnt area in [km^2]', 'value': 'burnt area [km2]'},
                             ],
                             value='burnt area [km2]',
                             multi=False,
                             clearable=False
                             ),

            ], className='six columns'),
        ], className='row'),

        html.Div([
            dcc.Graph(
                id='fires-in-2023',
                figure={},
                className='six columns'
            ),

            dcc.Graph(
                id='bar-graph',
                figure={},
                className='six columns'

            ),

        ], className='row')

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


@app.callback(
    Output('bar-graph', 'figure'),
    [Input('month-slider', 'value'),
     Input('bardropdown', 'value')]
)
def update_bar_graph(selected_month, bardropdown):
    filtered_df = df[df['month'] == selected_month]
    number_to_months = {6: 'June',
                        7: 'July',
                        8: 'August',
                        9: 'September',
                        10: 'October'}

    month_name = number_to_months.get(selected_month)
    fig = px.bar(data_frame=filtered_df,
                 x='state',
                 y=bardropdown,
                 title=f'Burnt area per state in {month_name}'
                 )

    fig.update_traces(marker_color='darkred',
                      marker_line_width=2, opacity=1)

    return fig


if __name__ == '__main__':
    app.run(debug=True)
