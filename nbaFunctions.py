import pandas as pd
import numpy as np
from basketball_reference_web_scraper import client
from player import *

#used the get the average of a player for the season
def average_stat_for_season(name):
    adv = pd.DataFrame(client.players_advanced_season_totals(season_end_year=2024))
    name = player(name,force_update=False)
    
    if name.empty:
        print(f"No data found for player: {name}")
        return None
    
    print(f"PPG:{name['PTS'].mean().round(1)} RPG:{name['REB'].mean().round(1)} APG:{name['AST'].mean().round(1)} FG%:{(name['FGM'].sum()/name['FGA'].sum()).round(2)}")

#used to calculate the amount of times they've hit the under in most recent games
def single_categories_stats(player_name, stat, projected_value, bet='over'):
    df = player(player_name, force_update=False)
    
    if stat not in df.columns:
        print(f"Stat '{stat}' not found in the data.")
        return None

    if df.empty:
        print(f"No data found for player: {player_name}")
        return None
    
    proj_value = np.ceil(projected_value) if bet =='over' else np.floor(projected_value)
    
    total_games_played = df.shape[0]
    if bet == 'under':
        tot_count = (df[stat] <= proj_value).sum()
    elif bet == 'over':
        tot_count = (df[stat] >= proj_value).sum()
    per = (tot_count/total_games_played * 100).round(1)
    
    intervals = [5,10,15]
    for num_games in intervals:
        player_data = df.tail(num_games)

        if bet == 'under':
            count = (player_data[stat] <= proj_value).sum()
        elif bet == 'over':
            count = (player_data[stat] >= proj_value).sum()

        percentage = (count / num_games * 100).round(1)
        print(f"The {bet} for {stat} hit {count}/{num_games} for {percentage}%")
    print(f"The {bet} for {stat} hit {tot_count}/{total_games_played} for {per}%")
    
#calculates the total for rebounds + assists + points
def pts_reb_asts(player_name,projected_value, bet='over'):
    df = player(player_name,force_update=False)

    if df.empty:
        print(f"No data found for player {player_name}")
        return None
    
    proj_value = np.ceil(projected_value) if bet == 'over' else np.floor(projected_value)
    total = df['PTS'] + df['AST'] + df['REB']
    
    total_games_played = df.shape[0]
    if bet == 'under':
        tot_count = (total <= proj_value).sum()
    elif bet == 'over':
        tot_count = (total >= proj_value).sum()
    per = (tot_count/total_games_played * 100).round(1)
    
    intervals = [5,10,15]
    for num_games in intervals:
        interval_data = df.tail(num_games)
        interval_total = interval_data['PTS'] + interval_data['AST'] + interval_data['REB']
        if bet == 'under':
            count = (interval_total <= proj_value).sum()
        elif bet == 'over':
            count = (interval_total >= proj_value).sum()

        percentage = (count / num_games * 100).round(1)
        print(f"The {bet} for PTS+AST+REB hit {count}/{num_games} for {percentage}%")
    print(f"The {bet} for PTS+AST+REB hit {tot_count}/{total_games_played} for {per}%")
    
#calculates the total for rebounds + points
def pts_reb(player_name,projected_value, bet='over'):
    df = player(player_name,force_update=False)

    if df.empty:
        print(f"No data found for player {player_name}")
        return None
    
    proj_value = np.ceil(projected_value) if bet == 'over' else np.floor(projected_value)
    total = df['PTS'] + df['REB']
    
    total_games_played = df.shape[0]
    if bet == 'under':
        tot_count = (total <= proj_value).sum()
    elif bet == 'over':
        tot_count = (total >= proj_value).sum()
    per = (tot_count/total_games_played * 100).round(1)
    
    intervals = [15,10,5]
    for num_games in intervals:
        interval_data = df.tail(num_games)
        interval_total = interval_data['PTS'] + interval_data['REB']
        if bet == 'under':
            count = (interval_total <= proj_value).sum()
        elif bet == 'over':
            count = (interval_total >= proj_value).sum()

        percentage = (count / num_games * 100).round(1)
        print(f"The {bet} for PTS+REB hit {count}/{num_games} for {percentage}%")
    print(f"The {bet} for PTS+REB hit {tot_count}/{total_games_played} for {per}%")
    
#calculates the total for assists + points
def pts_ast(player_name,projected_value, bet='over'):
    df = player(player_name,force_update=False)
    
    if df.empty:
        print(f"No data found for player {player_name}")
        return None
    
    proj_value = np.ceil(projected_value) if bet == 'over' else np.floor(projected_value)
    total = df['PTS'] + df['AST']
    
    total_games_played = df.shape[0]
    if bet == 'under':
        tot_count = (total <= proj_value).sum()
    elif bet == 'over':
        tot_count = (total >= proj_value).sum()
    per = (tot_count/total_games_played * 100).round(1)
    
    intervals = [5,10,15]
    for num_games in intervals:
        interval_data = df.tail(num_games)
        interval_total = interval_data['PTS'] + interval_data['AST']
        if bet == 'under':
            count = (interval_total <= proj_value).sum()
        elif bet == 'over':
            count = (interval_total >= proj_value).sum()

        percentage = (count / num_games * 100).round(1)
        print(f"The {bet} for PTS+AST hit {count}/{num_games} for {percentage}%")
    print(f"The {bet} for PTS+AST hit {tot_count}/{total_games_played} for {per}%")

#calculates the total for rebounds + assists
def reb_ast(player_name,projected_value, bet='over'):
    df = player(player_name,force_update=False)

    if df.empty:
        print(f"No data found for player {player_name}")
        return None
    
    proj_value = np.ceil(projected_value) if bet == 'over' else np.floor(projected_value)
    total = df['AST'] + df['REB']
    
    total_games_played = df.shape[0]
    if bet == 'under':
        tot_count = (total <= proj_value).sum()
    elif bet == 'over':
        tot_count = (total >= proj_value).sum()
    per = (tot_count/total_games_played * 100).round(1)
    
    intervals = [5,10,15]
    for num_games in intervals:
        interval_data = df.tail(num_games)
        interval_total = interval_data['AST'] + interval_data['REB']
        if bet == 'under':
            count = (interval_total <= proj_value).sum()
        elif bet == 'over':
            count = (interval_total >= proj_value).sum()

        percentage = (count / num_games * 100).round(1)
        print(f"The {bet} for AST+REB hit {count}/{num_games} for {percentage}%")
    print(f"The {bet} for AST+REB hit {tot_count}/{total_games_played} for {per}%")
 
#calculates the total for blocks + steals   
def blks_stls(player_name,projected_value, bet='over'):
    df = player(player_name,force_update=False)

    if df.empty:
        print(f"No data found for player {player_name}")
        return None
    
    proj_value = np.ceil(projected_value) if bet == 'over' else np.floor(projected_value)
    total = df['BLK'] + df['STL']
    
    total_games_played = df.shape[0]
    if bet == 'under':
        tot_count = (total <= proj_value).sum()
    elif bet == 'over':
        tot_count = (total >= proj_value).sum()
    per = (tot_count/total_games_played * 100).round(1)
    
    intervals = [5,10,15]
    for num_games in intervals:
        interval_data = df.tail(num_games)
        interval_total = interval_data['BLK'] + interval_data['STL']
        if bet == 'under':
            count = (interval_total <= proj_value).sum()
        elif bet == 'over':
            count = (interval_total >= proj_value).sum()

        percentage = (count / num_games * 100).round(1)
        print(f"The {bet} for BLK+STL hit {count}/{num_games} for {percentage}%")
    print(f"The {bet} for BLK+STL hit {tot_count}/{total_games_played} for {per}%")


def over_or_under():
    pass


def highest_to_lowest(array):
    #max player
    #if player is equal max append
    #return the array of players with highest percentage to hit 
    #make a function that allows me to check if the over or under is better 
    pass