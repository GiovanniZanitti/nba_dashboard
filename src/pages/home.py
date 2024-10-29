import dash
from dash import Dash, html, dcc, Output, Input, callback, clientside_callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from nba_api.stats.endpoints import scoreboardv2,leaguedashplayerstats, playergamelog,playergamelogs, leaguestandings
from datetime import datetime, date, timedelta
import pandas as pd

from mixins.functions_home import (
    get_game_header_score,
    game_card_best_players,
    game_card_score,
    player_card,
    df_to_dmc_table
)


dash.register_page(__name__, path='/')

def layout(**kwargs):

    div_return = [
        html.Div([
            dcc.DatePickerSingle(
                id='date-picker-input',
                date=date.today() - timedelta(days = 1)
            ),
            dcc.Store('data_game_header'),
            dmc.Grid([
                dmc.GridCol(html.Div(id='game_cards'),span=4),
                dmc.GridCol(html.Div(id='player_cards'),span=4),
                dmc.GridCol(html.Div(id='standings'),span=4)
            ])
            
        ],style={'margin-left':'15px','margin-right':'15px'})
    ]
    
    return div_return

@callback([Output('data_game_header','data'),Output('game_cards','children')],Input('date-picker-input','date'))
def update_data(date):
    games = scoreboardv2.ScoreboardV2(game_date=date).get_dict()['resultSets']
    df_game_header = pd.DataFrame(games[0]['rowSet'],columns=games[0]['headers'])
    df_line_score = pd.DataFrame(games[1]['rowSet'],columns=games[1]['headers'])
    df_best_players = pd.DataFrame(games[7]['rowSet'],columns=games[7]['headers'])
    df_game_header_score = get_game_header_score(df_game_header,df_line_score)
    div_return = [dmc.Divider(label='Games of the day',style={'margin-top':'15px'})]
    for index,row in df_game_header_score.iterrows():
        div_return += [
            dmc.Card(dcc.Link([
                game_card_score(row),
                game_card_best_players(row,df_best_players)
            ],href='/game_id/'+str(row['game_id']),style={"text-decoration": "none",'color':'#000000'}),
            withBorder=True,
            shadow="sm",
            radius="md",
            style={'margin-top':'15px'})
        ]
    return df_game_header.to_json(date_format='iso',orient='records'), div_return


@callback(Output('standings','children'),Input('date-picker-input','date'))
def update_data(date):
    standings = leaguestandings.LeagueStandings().get_data_frames()[0]
    div_return = []
    for conf in ['East','West']:
        div_return += [
            dmc.Divider(label=conf+'ern conference',variant="solid",style={'margin-top':'15px'}),
            dmc.Card(
                df_to_dmc_table(standings[standings['Conference'] == conf][['TeamName','PlayoffRank','Record','WinPCT','CurrentStreak']].reset_index(drop=True)),
                withBorder=True,
                shadow="sm",
                radius="md",
                style={'margin-top':'15px'}
            )
        ]

    return div_return


@callback(Output('player_cards','children'),Input('date-picker-input','date'))
def update_data(date):
    df_players_stats = leaguedashplayerstats.LeagueDashPlayerStats(per_mode_detailed='PerGame').get_data_frames()[0]
    df_players_log = playergamelogs.PlayerGameLogs(last_n_games_nullable=3,season_nullable='2024-25').get_data_frames()[0]
    french_players = [1641705,1642258,1627824]
    player_div_return = [dmc.Divider(label='Favorite players',variant="solid",style={'margin-top':'15px'})]
    for index,row in df_players_stats[df_players_stats['PLAYER_ID'].isin(french_players)].iterrows():
        game_log = df_players_log[df_players_log['PLAYER_ID'] == row['PLAYER_ID']].reset_index(drop=True)
        player_div_return += [
            player_card(row,game_log)  
        ]
    player_div_return += [dmc.Divider(label='Top players',variant="solid",style={'margin-top':'15px'})]
    for index,row in df_players_stats.sort_values('NBA_FANTASY_PTS_RANK').head(20).iterrows():
        game_log = df_players_log[df_players_log['PLAYER_ID'] == row['PLAYER_ID']].reset_index(drop=True)
        player_div_return += [
            player_card(row,game_log)  
        ]
    
    return player_div_return








