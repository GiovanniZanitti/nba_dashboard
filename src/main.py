# -*- coding: utf-8 -*-
from app import app, server
import dash
from dash import Dash, html, dcc, dash_table, Input, Output, callback, no_update
import pandas as pd
import dash_mantine_components as dmc



app.layout = dmc.MantineProvider(
    html.Div([
        dmc.AppShell(
            children=[
                dmc.AppShellHeader([
                    html.Div([
                        dcc.Link(
                            dmc.Image(src='https://cdn.nba.com/logos/leagues/logo-nba.svg',style={'margin':'15px'}),
                            href='/'
                        ),
                    ], style={'display': 'flex', 'align-items': 'center', 'width': '100%'})
                ],style={'background-color':'#1E75DF'})
            ]
        ),
        html.Div([
            html.Div(dash.page_container)
        ],style={'margin-top':'5.3rem'})
    ])
)

if __name__ == '__main__':
    app.run_server(debug=True,dev_tools_props_check=False)