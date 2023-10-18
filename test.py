import json

from dash import Dash, dcc, html
import plotly.graph_objects as go
import geopandas as gpd

import plotly.express as px
import pandas as pd

df = px.data.election()
geojson = px.data.election_geojson()

print(df.head())
# print(geojson)

