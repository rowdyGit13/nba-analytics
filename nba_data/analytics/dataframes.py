"""
Module for building pandas DataFrames from NBA data models.
These functions transform Django model instances into analysis-ready pandas DataFrames.
"""

import pandas as pd
#from django.db.models import F, Q, Count, Avg, Sum, Case, When, Value, IntegerField
from nba_data.models import Team, Player, Game

def get_teams_dataframe():
    """
    Retrieve all teams and convert to a pandas DataFrame.
    
    Returns:
        pandas.DataFrame: DataFrame containing team information
    """
    teams = Team.objects.all().values(
        'team_id', 'abbreviation', 'city', 'conference', 'division', 'full_name', 'name'
    )
    
    if not teams:
        return pd.DataFrame()
    
    df = pd.DataFrame(list(teams))
    
    return df

def get_players_dataframe():
    """
    Retrieve all players with team information and convert to a pandas DataFrame.
    
    Returns:
        pandas.DataFrame: DataFrame containing player information with team details
    """
# Players.objects accesses the Player model
# select_related('team') accesses the team related to the player linked via a foreign key, preventing
# the need to make a separate query to retrieve the team data.
# values() is used to retrieve specific fields from the model instances (objects)
# Fields like 'player_id', 'first_name', 'last_name', etc., are directly from the Player model.
# Fields prefixed with team__ (e.g., 'team__team_id', 'team__abbreviation') are retrieved from the related Team model.
# The double underscore (__) is Django's syntax for traversing relationships.

# In esssence, this block constructs a database query to fetch a list of dictionaries. Each dictionary contains the specified 
# details for a player, including relevant information about the team they belong to, retrieved efficiently in a single database operation.

    players = Player.objects.select_related('team').values(
        'player_id', 'first_name', 'last_name', 'position', 
        'height_feet', 'height_inches', 'height_total_inches',      
        'weight_pounds', 'jersey_number', 'college', 'country',
        'draft_year', 'draft_round', 'draft_number',
        'team__team_id', 'team__abbreviation',
        'team__full_name', 'team__conference', 'team__division'
    )
    
    if not players:
        return pd.DataFrame()
    
    df = pd.DataFrame(list(players))
    
    # Rename team-related columns for clarity
    if 'team__team_id' in df.columns:
        team_columns = {
            'team__team_id': 'team_id',
            'team__abbreviation': 'team_abbreviation',
            'team__full_name': 'team_name',
            'team__conference': 'team_conference',
            'team__division': 'team_division'
        }
        df = df.rename(columns=team_columns)
    
    # Add full name as a convenience column
    df['full_name'] = df['first_name'] + ' ' + df['last_name']
    
    return df

def get_games_dataframe():
    """
    Retrieve all games with team information and convert to a pandas DataFrame.
    
    Returns:
        pandas.DataFrame: DataFrame containing game information with team details
    """
    # Game.objects accesses the Game model
    # select_related() joins the home_team and visitor_team tables to avoid additional queries
    # values() specifies which fields to retrieve from Game and related Team models
    # Fields like game_id, date, etc. come directly from Game model
    # Fields with home_team__ or visitor_team__ prefix come from the related Team models
    # This creates an efficient single query to get game data with both teams' information
    games = Game.objects.select_related('home_team', 'visitor_team').values(
        'game_id', 'date', 'datetime',
        'season', 'status', 'period', 'time', 'postseason', 
        'home_team_score', 'visitor_team_score',
        'home_team__team_id', 'home_team__conference', 'home_team__full_name',
        'visitor_team__team_id', 'visitor_team__conference', 'visitor_team__full_name'
    )
    
    if not games:
        return pd.DataFrame()
    
    df = pd.DataFrame(list(games))
    
    # Rename team-related columns for clarity
    if 'home_team__team_id' in df.columns:
        team_columns = {
            'home_team__team_id': 'home_team_id',
            'home_team__conference': 'home_team_conference',
            'home_team__full_name': 'home_team_name',
            'visitor_team__team_id': 'visitor_team_id',
            'visitor_team__conference': 'visitor_team_conference',
            'visitor_team__full_name': 'visitor_team_name'
        }
        df = df.rename(columns=team_columns)
            
    return df