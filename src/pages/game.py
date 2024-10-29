import dash
from dash import Dash, html, dcc, Output, Input, callback, clientside_callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.endpoints import playbyplayv2
from datetime import datetime, date, timedelta


import pandas as pd


dash.register_page(__name__, path_template='/game_id/<game_id>')

def layout(game_id,**kwargs):
    game = boxscore.BoxScore(game_id).get_dict()['game']
    play_by_play = playbyplayv2.PlayByPlayV2(game_id).get_data_frames()[0]
    df_play_by_play = get_play_by_play_df(play_by_play)

    div_return = html.Div([
        dcc.Store(id='data_score_diff',data=df_play_by_play.to_json(date_format='iso',orient='records')),
        dbc.Row([
            dbc.Col([
                card
            ], xs=10, sm=10, md=4, lg=3, xl=3)
            for card in [game_card_score(game),game_card_area_graph_score_diff()]
        ]),
    ],style={'margin-left':'15px'})
    
    return div_return


# Clientside Callback pour appeler la fonction JavaScript dans echart_score_diff.js
clientside_callback(
    """
    function(echartsData) {
        window.dash_clientside.echartsScoreDiff.ScoreDiff(echartsData);
        return window.dash_clientside.no_update;
    }
    """,
    output=Output('echarts_area_score_diff','children'),
    inputs=Input('data_score_diff','data'),
)


def game_card_area_graph_score_diff():
    div_return = dmc.Card(
        html.Div(id='echarts_area_score_diff', style={'height': '100%', 'width': '100%', 'display': 'flex'}),
        withBorder=True,
        shadow="sm",
        radius="md",
        style={'height': '100px'}  # Spécifiez la hauteur ici
    )
    return div_return

def game_card_score(game):
    div_return = dmc.Card(
        dmc.Grid([
            dmc.GridCol([
                dmc.Image(src='https://cdn.nba.com/logos/nba/'+str(game['awayTeam']['teamId'])+'/global/L/logo.svg')
            ],span=3),
            dmc.GridCol([
                dmc.Flex(
                    children=[
                        dmc.Center(str(game['awayTeam']['score']))
                    ],
                    justify="center",  # Centre horizontalement
                    align="center",    # Centre verticalement
                    style={"height": "100%"}  # Assure que la flexbox prend toute la hauteur disponible
                )
            ],span=2),
            dmc.GridCol([
                dmc.Flex(
                    children=[
                        dmc.Center(' - ')
                    ],
                    justify="center",  # Centre horizontalement
                    align="center",    # Centre verticalement
                    style={"height": "100%"}  # Assure que la flexbox prend toute la hauteur disponible
                )
            ],span=2),
            dmc.GridCol([
                dmc.Flex(
                    children=[
                        dmc.Center(str(game['homeTeam']['score']))
                    ],
                    justify="center",  # Centre horizontalement
                    align="center",    # Centre verticalement
                    style={"height": "100%"}  # Assure que la flexbox prend toute la hauteur disponible
                )
            ],span=2),
            dmc.GridCol([
                dmc.Image(src='https://cdn.nba.com/logos/nba/'+str(game['homeTeam']['teamId'])+'/global/L/logo.svg')
            ],span=3),
        ]),
        withBorder=True,
        shadow="sm",
        radius="md",
    )
    return div_return


def get_play_by_play_df(df):
    play_by_play_df = df[['PCTIMESTRING', 'PERIOD', 'SCORE', 'HOMEDESCRIPTION', 'VISITORDESCRIPTION']]

    # Étape 3 : Convertir le temps de chaque période en temps cumulé en minutes
    def calculate_total_time(row):
        minutes, seconds = map(int, row['PCTIMESTRING'].split(":"))
        period_offset = (row['PERIOD'] - 1) * 12  # Chaque période ajoute 12 minutes
        return period_offset + (12 - minutes) - (seconds / 60)  # Temps écoulé en minutes

    play_by_play_df['TOTAL_MINUTES'] = play_by_play_df.apply(calculate_total_time, axis=1)

    # Étape 4 : Extraire les scores et remplir les valeurs manquantes
    # Remplir les scores et les diviser en home et away
    play_by_play_df['HOME_SCORE'] = play_by_play_df['SCORE'].apply(lambda x: int(x.split(" - ")[0]) if pd.notna(x) else None)
    play_by_play_df['AWAY_SCORE'] = play_by_play_df['SCORE'].apply(lambda x: int(x.split(" - ")[1]) if pd.notna(x) else None)

    # Remplir les valeurs manquantes pour obtenir l’évolution complète du score
    play_by_play_df['HOME_SCORE'].ffill(inplace=True)
    play_by_play_df['AWAY_SCORE'].ffill(inplace=True)
    play_by_play_df[['HOME_SCORE', 'AWAY_SCORE']] = play_by_play_df[['HOME_SCORE', 'AWAY_SCORE']].fillna(0)

    # Calculer l'écart de score
    play_by_play_df['SCORE_DIFF'] = play_by_play_df['HOME_SCORE'] - play_by_play_df['AWAY_SCORE']

    # Étape 5 : Filtrer pour garder les lignes où SCORE est non null
    score_changes = play_by_play_df.dropna(subset=['SCORE']).reset_index(drop=True)

    # Ajouter un point de départ à 0 minute avec un écart de score de 0
    start_point = pd.DataFrame({'TOTAL_MINUTES': [0], 'SCORE_DIFF': [0]})
    score_changes = pd.concat([start_point, score_changes], ignore_index=True)

    # Convertir TOTAL_MINUTES en format mm:ss
    score_changes['TOTAL_MINUTES'] = score_changes['TOTAL_MINUTES'].apply(lambda x: f"{int(x):02d}:{int((x % 1) * 60):02d}")

    return play_by_play_df