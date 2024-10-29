import dash
import dash_mantine_components as dmc
from dash import Dash, _dash_renderer
_dash_renderer._set_react_version("18.2.0")
import pandas as pd
import dash_bootstrap_components as dbc


app = Dash(
    __name__, 
    use_pages=True, 
    external_stylesheets=[dbc.themes.BOOTSTRAP,dmc.styles.ALL,dmc.styles.DATES],
    external_scripts=['https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js']
    )
server = app.server
