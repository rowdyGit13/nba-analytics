from .dataframes import (
    get_teams_dataframe,
    get_players_dataframe, 
    get_games_dataframe
)
from .data_prep import (
    clean_games_data,
    clean_player_data,
    clean_teams_data,
    enhance_game_data,
    prepare_home_vs_away
)
from .stats import (
    calculate_team_performance_metrics,
    calculate_team_rankings,
    calculate_league_averages,
)
import pandas as pd


def get_team_stats(season=None):
    """
    Get comprehensive team statistics and metrics.
    
    Args:
        season (int, optional): Season to filter data for (e.g., 2022 for 2022-2023 season)
        
    Returns:
        pandas.DataFrame: Team statistics with performance metrics
    """
    # Get raw data
    games_df = get_games_dataframe()
    games_df = clean_games_data(games_df)
    # Filter by season if specified
    if season and 'season' in games_df.columns:
        games_df = games_df[games_df['season'] == season]
    
    # Calculate team statistics
    prepared_games_df = enhance_game_data(games_df)
    team_stats_df = prepare_home_vs_away(prepared_games_df)
    
    # Calculate advanced metrics
    team_metrics_df = calculate_team_performance_metrics(team_stats_df)
    
    return team_metrics_df


def get_team_rankings(season=None):
    """
    Get team rankings based on various performance metrics.
    
    Args:
        season (int, optional): Season to filter data for
        
    Returns:
        pandas.DataFrame: Team rankings for various metrics
    """
    team_metrics_df = get_team_stats(season)
    rankings_df = calculate_team_rankings(team_metrics_df, season)
    
    return rankings_df

def get_league_overview(season=None):
    """
    Get league-wide statistics and averages.
    
    Args:
        season (int, optional): Season to filter data for
        
    Returns:
        dict: League-wide statistics and averages
    """
    # Get necessary data
    games_df = get_games_dataframe()
    
    # Filter by season if specified
    if season and 'season' in games_df.columns:
        games_df = games_df[games_df['season'] == season]
    
    prepared_games_df = enhance_game_data(games_df)
    team_stats_df = prepare_home_vs_away(prepared_games_df)
    team_metrics_df = calculate_team_performance_metrics(team_stats_df)
    
    # Calculate league averages
    league_averages = calculate_league_averages(prepared_games_df, team_metrics_df)
    
    return league_averages


def get_team_game_log(team_id, season=None):
    """
    Get a team's game log for a specific season.
    
    Args:
        team_id (int): Team ID
        season (int, optional): Season to filter data for
        
    Returns:
        pandas.DataFrame: Team's game log
    """
    games_df = get_games_dataframe()
    
    # Filter by season if specified
    if season and 'season' in games_df.columns:
        games_df = games_df[games_df['season'] == season]
    
    # Prepare game data
    prepared_games_df = enhance_game_data(games_df)
    
    # Filter for the specific team (either as home or visitor)
    home_games = prepared_games_df[prepared_games_df['home_team_id'] == team_id]
    away_games = prepared_games_df[prepared_games_df['visitor_team_id'] == team_id]
    
    # Combine home and away games
    team_games = pd.concat([home_games, away_games]).sort_values('date')
    
    return team_games


def get_head_to_head(team1_id, team2_id, season=None):
    """
    Get head-to-head matchup data between two teams.
    
    Args:
        team1_id (int): First team ID
        team2_id (int): Second team ID
        season (int, optional): Season to filter data for
        
    Returns:
        pandas.DataFrame: Head-to-head matchup data
    """
    games_df = get_games_dataframe()
    
    # Filter by season if specified
    if season and 'season' in games_df.columns:
        games_df = games_df[games_df['season'] == season]
    
    # Find games between the two teams
    team1_home = games_df[(games_df['home_team_id'] == team1_id) & 
                          (games_df['visitor_team_id'] == team2_id)]
    team2_home = games_df[(games_df['home_team_id'] == team2_id) & 
                          (games_df['visitor_team_id'] == team1_id)]
    
    # Combine all matchups
    matchups = pd.concat([team1_home, team2_home]).sort_values('date')
    
    # Prepare game data
    if not matchups.empty:
        return enhance_game_data(matchups)
    
    return pd.DataFrame()