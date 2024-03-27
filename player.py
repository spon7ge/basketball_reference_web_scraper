import pandas as pd
import numpy as np
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Location 
from basketball_reference_web_scraper.data import Team
from basketball_reference_web_scraper.data import Outcome 
from basketball_reference_web_scraper.data import OutputType  
from basketball_reference_web_scraper.data import OutputWriteOption 
from basketball_reference_web_scraper.data import Position
from datetime import datetime, timedelta, date
import time
import json

#json file name 
cache_file_path = 'players_cache.json'

#loads json file
def load_cache():
    try:
        with open(cache_file_path, 'r') as file:
            return json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
        return {}

def date_converter(o):
    if isinstance(o, (date, datetime)):
        return o.isoformat()

def save_cache(cache):
    with open(cache_file_path, 'w') as file:
        json.dump(cache, file, default=date_converter, indent=4)

#Grabs player data
def player(name, force_update=False):
    cache = load_cache()
    year = 2024 

    slug = getPlayerSlug(name)
    if slug is None:
        print(f"Player name {name} not found in CSV.")
        return pd.DataFrame()
    
    if not force_update and slug in cache and str(year) in cache[slug]:
        return pd.DataFrame(cache[name][str(year)])
    elif not force_update:
        # If force_update is False and the data is not in the cache, return None or raise an error
        return pd.DataFrame()
    
    data = pd.DataFrame(client.regular_season_player_box_scores(
        player_identifier=slug, 
        season_end_year=year
    ))
    
    if 'date' in data.columns: 
        data['date'] = data['date'].apply(lambda x: x.isoformat() if isinstance(x, (date, datetime)) else x)

    if 'team' in data.columns:
        data['team'] = data['team'].apply(lambda x: x.name if isinstance(x, Team) else x)
    if 'location' in data.columns:
        data['location'] = data['location'].apply(lambda x: x.name if isinstance(x, Location) else x)
    if 'opponent' in data.columns:
        data['opponent'] = data['opponent'].apply(lambda x: x.name if isinstance(x, Team) else x)
    if 'outcome' in data.columns:
        data['outcome'] = data['outcome'].apply(lambda x: x.name if isinstance(x, Outcome) else x)
        
    data['total_rebounds'] = data['offensive_rebounds'] + data['defensive_rebounds']
    
    data.rename(columns={
        'games_played': 'GP',
        'made_field_goals': 'FGM',
        'attempted_field_goals': 'FGA',
        'made_three_point_field_goals': '3PTM',
        'attempted_three_point_field_goals': '3PTA',
        'made_free_throws': 'FTM',
        'attempted_free_throws': 'FTA',
        'offensive_rebounds': 'OREB',
        'defensive_rebounds': 'DREB',
        'personal_fouls': 'PF',
        'assists': 'AST',
        'steals':'STL',
        'blocks':'BLK',
        'turnovers':'TOV',
        'points_scored': 'PTS',
        'game_score': 'game score',
        'plus_minus': '+/-',
        'total_rebounds': 'REB'
        
    }, inplace=True)
    
    column_order = ['date', 'team', 'location', 'opponent', 'outcome', 'active','seconds_played', 'FGM', 'FGA', '3PTM', '3PTA', 'FTM', 'FTA','REB','OREB','DREB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'game score', '+/-']
    data = data[column_order]

    if slug not in cache:
        cache[slug] = {}
    cache[slug][str(year)] = data.to_dict('records')
    
    save_cache(cache)
    
    return data

def update_player_cache(name):
    return player(name, force_update=True)

#updates the current csv file if anyone new was added during the season 
df = pd.DataFrame(client.players_season_totals(season_end_year=2024)) #use this to check if anyone new has been added to the dataset
def update_players_csv(file, csv_path='player_slugs.csv'):
    # Load the existing data if the CSV exists, otherwise create an empty DataFrame
    try:
        existing_df = pd.read_csv(csv_path)
        existing_dict = pd.Series(existing_df.name.values, index=existing_df.slug).to_dict()
    except FileNotFoundError:
        existing_df = pd.DataFrame(columns=['slug', 'name'])
        existing_dict = {}
    
    # Flag to check if the CSV needs updating
    update_needed = False

    for index, row in file.iterrows():
        slug = row['slug']
        name = row['name'].lower().replace(' jr.', '').replace(' sr.', '').replace(' iii', '').replace(' ii', '').replace('iv', '').replace('ć','c').replace('č','c').replace('é', 'e').replace('ā', 'a').strip()
        # If the player is not in the existing data, add them
        if slug not in existing_dict:
            update_needed = True
            existing_dict[slug] = name
            existing_df = existing_df.append({'slug': slug, 'name': name}, ignore_index=True)

    # Update the CSV file if there are new players
    if update_needed:
        existing_df.to_csv(csv_path, index=False)
        print("CSV file has been updated.")
    else:
        print("No updates are needed for the CSV file.")

#gets the unique slug name for each player
def getPlayerSlug(name):
    player = find_player_by_full_name(name)
    if player:
        return player
    else:
        return f"{name} is not valid or not in CSV file." 

#finds the player in the CSV file    
def find_player_by_full_name(name):
    df = pd.read_csv('player_slugs.csv')
    matched_row = df[df['name'] == name]
    if not matched_row.empty:
        return matched_row.iloc[0]['slug']
    else:
        return None