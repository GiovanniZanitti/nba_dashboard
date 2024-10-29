import dash_mantine_components as dmc
from nba_api.stats.endpoints import scoreboardv2,leaguedashplayerstats, playergamelog,playergamelogs, leaguestandings
from datetime import datetime, date, timedelta
from dash import Dash, html, dcc, Output, Input, callback, clientside_callback


import pandas as pd

def get_game_header_score(df_game_header,df_line_score):
    df_game_header_score = pd.DataFrame()
    for game_id in set(df_line_score['GAME_ID']):
        home_team_id = df_game_header[df_game_header['GAME_ID'] == game_id]['HOME_TEAM_ID'].item()
        away_team_id = df_game_header[df_game_header['GAME_ID'] == game_id]['VISITOR_TEAM_ID'].item()
        row = pd.DataFrame({
            'game_id':game_id,
            'home_team_id': home_team_id,
            'home_team_name': df_line_score[df_line_score['TEAM_ID'] == home_team_id]['TEAM_NAME'].item(),
            'home_team_score': df_line_score[df_line_score['TEAM_ID'] == home_team_id]['PTS'].item(),
            'away_team_score': df_line_score[df_line_score['TEAM_ID'] == away_team_id]['PTS'].item(),
            'away_team_name': df_line_score[df_line_score['TEAM_ID'] == away_team_id]['TEAM_NAME'].item(),
            'away_team_id':away_team_id
        },index=[0])
        df_game_header_score = pd.concat([df_game_header_score,row])
    return df_game_header_score

def game_card_score(row_df_game_header_score):
    row = row_df_game_header_score.copy()
    div_return = dmc.Grid([
        dmc.GridCol([
            dmc.Image(src='https://cdn.nba.com/logos/nba/'+str(row['away_team_id'])+'/global/L/logo.svg')
        ],span=3),
        dmc.GridCol([
            dmc.Flex(
                children=[
                    dmc.Center(str(row['away_team_score']))
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
                    dmc.Center(str(row['home_team_score']))
                ],
                justify="center",  # Centre horizontalement
                align="center",    # Centre verticalement
                style={"height": "100%"}  # Assure que la flexbox prend toute la hauteur disponible
            )
        ],span=2),
        dmc.GridCol([
            dmc.Image(src='https://cdn.nba.com/logos/nba/'+str(row['home_team_id'])+'/global/L/logo.svg')
        ],span=3),
    ])
    
    return div_return


def game_card_best_players(row,df_best_players):
    row['home_team_id']
    div_return = html.Div([
        dmc.Grid([
            dmc.GridCol(df_best_players[df_best_players['TEAM_ID'] == row['away_team_id']]['PTS_PLAYER_NAME'],span=3),
            dmc.GridCol(flex(df_best_players[df_best_players['TEAM_ID'] == row['away_team_id']]['PTS']),span=2),
            dmc.GridCol(flex('PTS'),span=2),
            dmc.GridCol(flex(df_best_players[df_best_players['TEAM_ID'] == row['home_team_id']]['PTS']),span=2),
            dmc.GridCol(df_best_players[df_best_players['TEAM_ID'] == row['home_team_id']]['PTS_PLAYER_NAME'],style={'text-align':'right'},span=3) 
        ]),
        dmc.Grid([
            dmc.GridCol(df_best_players[df_best_players['TEAM_ID'] == row['away_team_id']]['REB_PLAYER_NAME'],span=3),
            dmc.GridCol(flex(df_best_players[df_best_players['TEAM_ID'] == row['away_team_id']]['REB']),span=2),
            dmc.GridCol(flex('PTS'),span=2),
            dmc.GridCol(flex(df_best_players[df_best_players['TEAM_ID'] == row['home_team_id']]['REB']),span=2),
            dmc.GridCol(df_best_players[df_best_players['TEAM_ID'] == row['home_team_id']]['REB_PLAYER_NAME'],style={'text-align':'right'},span=3) 
        ]),
        dmc.Grid([
            dmc.GridCol(df_best_players[df_best_players['TEAM_ID'] == row['away_team_id']]['AST_PLAYER_NAME'],span=3),
            dmc.GridCol(flex(df_best_players[df_best_players['TEAM_ID'] == row['away_team_id']]['AST']),span=2),
            dmc.GridCol(flex('PTS'),span=2),
            dmc.GridCol(flex(df_best_players[df_best_players['TEAM_ID'] == row['home_team_id']]['AST']),span=2),
            dmc.GridCol(df_best_players[df_best_players['TEAM_ID'] == row['home_team_id']]['AST_PLAYER_NAME'],style={'text-align':'right'},span=3) 
        ])
    ],style={'font-size':'10px'})
    return div_return


def flex(div):
    return dmc.Flex(
        children=[
            dmc.Center(div)
        ],
        justify="center",  # Centre horizontalement
        align="center",    # Centre verticalement
        style={"height": "100%"}  # Assure que la flexbox prend toute la hauteur disponible
    )


def player_card(row,game_log):
    return dmc.Card([
        dmc.Grid([
            dmc.GridCol([
                dmc.Image(src='https://cdn.nba.com/headshots/nba/latest/260x190/'+str(row['PLAYER_ID'])+'.png'),
                dmc.Text(row['PLAYER_NAME'],style={'text-align':'center','margin-top':'15px'})
            ],span=3),
            dmc.GridCol([
                dmc.Grid([
                    dmc.GridCol('',span=2),
                    dmc.GridCol('PTS',span=2),
                    dmc.GridCol('REB',span=2),
                    dmc.GridCol('AST',span=2),
                    dmc.GridCol('STL',span=2),
                    dmc.GridCol('BLK',span=2),
                ],style={'font-size':'10px'}),
                dmc.Grid([
                    dmc.GridCol('AVG',span=2),
                    dmc.GridCol(row['PTS'],span=2),
                    dmc.GridCol(row['REB'],span=2),
                    dmc.GridCol(row['AST'],span=2),
                    dmc.GridCol(row['STL'],span=2),
                    dmc.GridCol(row['BLK'],span=2)
                ]),
                dmc.Center(dmc.Text('Last games',style={'font-size':'8px'},c='dimmed'),style={'margin':'8px'}),
                dmc.Grid([
                    dmc.GridCol(game_log['MATCHUP'][0][4:],style={'font-size':'8px','display': 'flex', 'align-items': 'center'},span=2),
                    dmc.GridCol(game_log['PTS'][0],style={'display': 'flex', 'align-items': 'center'},span=2),
                    dmc.GridCol(game_log['REB'][0],style={'display': 'flex', 'align-items': 'center'},span=2),
                    dmc.GridCol(game_log['AST'][0],style={'display': 'flex', 'align-items': 'center'},span=2),
                    dmc.GridCol(game_log['STL'][0],style={'display': 'flex', 'align-items': 'center'},span=2),
                    dmc.GridCol(game_log['BLK'][0],style={'display': 'flex', 'align-items': 'center'},span=2)
                ],style={'font-size':'10px'}),
                dmc.Grid([
                    dmc.GridCol(game_log['MATCHUP'][1][4:],style={'font-size':'8px','display': 'flex', 'align-items': 'center'},span=2),
                    dmc.GridCol(game_log['PTS'][1],style={'display': 'flex', 'align-items': 'center'},span=2),
                    dmc.GridCol(game_log['REB'][1],style={'display': 'flex', 'align-items': 'center'},span=2),
                    dmc.GridCol(game_log['AST'][1],style={'display': 'flex', 'align-items': 'center'},span=2),
                    dmc.GridCol(game_log['STL'][1],style={'display': 'flex', 'align-items': 'center'},span=2),
                    dmc.GridCol(game_log['BLK'][1],style={'display': 'flex', 'align-items': 'center'},span=2)
                ],style={'font-size':'10px'}),
                # dmc.Grid([
                #     dmc.GridCol(game_log['MATCHUP'][2][4:],style={'font-size':'8px','display': 'flex', 'align-items': 'center'},span=2),
                #     dmc.GridCol(game_log['PTS'][2],style={'display': 'flex', 'align-items': 'center'},span=2),
                #     dmc.GridCol(game_log['REB'][2],style={'display': 'flex', 'align-items': 'center'},span=2),
                #     dmc.GridCol(game_log['AST'][2],style={'display': 'flex', 'align-items': 'center'},span=2),
                #     dmc.GridCol(game_log['STL'][2],style={'display': 'flex', 'align-items': 'center'},span=2),
                #     dmc.GridCol(game_log['BLK'][2],style={'display': 'flex', 'align-items': 'center'},span=2)
                # ],style={'font-size':'10px'})
            ],span=9)
        ])
        
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={'margin-top':'15px'})

def df_to_dmc_table(df, table_caption="Data Table"):
    """
    Transform a pandas DataFrame into a Dash Mantine Components (DMC) Table.
    
    Parameters:
        df (pandas.DataFrame): The DataFrame to convert.
        table_caption (str): Optional caption for the table.
    
    Returns:
        dmc.Table: The generated table.
    """
    # Create table header dynamically based on the DataFrame columns
    head = dmc.TableThead(
        dmc.TableTr(
            [dmc.TableTh(col) for col in df.columns]  # Create a table header for each column
        )
    )

    # Create table body dynamically by iterating over each row in the DataFrame
    # Crée les lignes de données
    rows = []
    for idx, row in df.iterrows():
        row_cells = []
        for i, cell in enumerate(row):
            # Définit l'alignement : à gauche pour la première colonne, à droite pour les autres
            cell_alignment = "left" if i == 0 else "right"
            cell_content = (
                html.Img(src=cell, style={"width": "50px", "height": "50px"})
                if isinstance(cell, str) and cell.startswith("http")
                else cell
            )
            row_cells.append(html.Td(cell_content, style={"textAlign": cell_alignment}))

        # Applique un style de fond pour alterner les lignes
        row_style = {"backgroundColor": "#f9f9f9"} if idx % 2 == 0 else {"backgroundColor": "#ffffff"}
        rows.append(html.Tr(row_cells, style=row_style))

    body = dmc.TableTbody(rows)
    caption = dmc.TableCaption(table_caption)

    # Return the DMC Table
    return dmc.Table([head, body],striped=True,style={'font-size':'12px'})