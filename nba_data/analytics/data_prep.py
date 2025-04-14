"""
Module for cleaning and transforming NBA data.
These functions perform data preparation tasks needed before analysis.
"""

import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_player_data(df):
    """
    Clean the player DataFrame by handling missing values and standardizing field formats.
    
    Args:
        df (pandas.DataFrame): DataFrame containing player data
        
    Returns:
        pandas.DataFrame: Cleaned player DataFrame
    """
    if df.empty:
        return df
    
    # Make a copy to avoid modifying the original
    cleaned_df = df.copy()
    
    # Standardize position data
    if 'position' in cleaned_df.columns:
        # Map variations to standard positions
        position_map = {
            'G': 'G', 'SG': 'G', 'PG': 'G', 'Guard': 'G',
            'F': 'F', 'SF': 'F', 'PF': 'F', 'Forward': 'F',
            'C': 'C', 'Center': 'C',
            'G-F': 'G-F', 'F-G': 'G-F', 
            'F-C': 'F-C', 'C-F': 'F-C'
        }
        
        # Apply mapping and handle missing/unknown values
        cleaned_df['position_standard'] = cleaned_df['position'].map(
            lambda x: position_map.get(x, x) if pd.notna(x) else 'Unknown'
        )
    
    # Handle missing height/weight data
    for col in ['height_feet', 'height_inches', 'height_total_inches', 'weight_pounds']:
        if col in cleaned_df.columns:
            # Replace missing values with NaN for consistency
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
    
    return cleaned_df

def clean_teams_data(df):
    """
    Clean the team  DataFrame by handling missing values and standardizing field formats.
    
    Args:
        df (pandas.DataFrame): DataFrame containing team data
        
    Returns:
        pandas.DataFrame: Cleaned team DataFrame
    """
    if df.empty:
        return df
    
    # Make a copy to avoid modifying the original
    cleaned_df = df.copy()
    
    # Standardize conference data
    if 'conference' in cleaned_df.columns:
        # Map variations to standard positions
        conference_map = {
            'East': 'East', 'West': 'West',
            'East Conference': 'East', 'West Conference': 'West',
            'Eastern Conference': 'East', 'Western Conference': 'West',
        }
        
        # Apply mapping and handle missing/unknown values
        cleaned_df['conference_standard'] = cleaned_df['conference'].map(
            lambda x: conference_map.get(x, x) if pd.notna(x) else 'Unknown'
        )
    
    # Handle missing abbreviation data
    for col in ['abbreviation']:
        if col in cleaned_df.columns:
            # Replace missing values with NaN for consistency
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
    
    return cleaned_df

def clean_games_data(df):
    """
    Clean the games DataFrame by handling missing values and standardizing field formats.
    
    Args:
        df (pandas.DataFrame): DataFrame containing games data
        
    Returns:
        pandas.DataFrame: Cleaned games DataFrame
    """
    if df.empty:
        return df
    
    # Make a copy to avoid modifying the original
    cleaned_df = df.copy()
    
    # Standardize date data to format YYYY-MM-DD
    if 'date' in cleaned_df.columns:
        cleaned_df['date'] = pd.to_datetime(cleaned_df['date'])
    
    # Handle missing datetime data
    for col in ['datetime']:
        if col in cleaned_df.columns:
            # Replace missing values with NaN for consistency
            cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors='coerce')
            
    # Ensure season is in YYYY-YYYY format
    if 'season' in cleaned_df.columns and not cleaned_df.empty:
        # Process each row individually to handle mixed formats
        def format_season(season):
            if isinstance(season, str) and '-' in season:
                # Already in YYYY-YYYY format
                return season
            elif isinstance(season, (int, float)) or (isinstance(season, str) and season.isdigit()):
                # Convert to int and then to YYYY-YYYY format
                season_int = int(float(season))
                return f"{season_int}-{season_int+1}"
            else:
                # Just return as is if we can't process it
                return season
            
        cleaned_df['season'] = cleaned_df['season'].apply(format_season)
    
    return cleaned_df

def enhance_game_data(df):
    """
    Prepare the game DataFrame by adding derived metrics.
    
    Args:
        df (pandas.DataFrame): DataFrame containing game data
        
    Returns:
        pandas.DataFrame: Enhanced game DataFrame with derived metrics
    """
    logger.info("Initial game DataFrame shape: %s", df.shape)
    
    if df.empty:
        return df
    
    # Make a copy to avoid modifying the original
    enhanced_df = df.copy()
    
    # Calculate point differential
    if all(col in enhanced_df.columns for col in ['home_team_score', 'visitor_team_score']):
        enhanced_df['point_diff'] = enhanced_df['home_team_score'] - enhanced_df['visitor_team_score']
        enhanced_df['total_points'] = enhanced_df['home_team_score'] + enhanced_df['visitor_team_score']
    
    # Add win/loss indicator for home team
    if 'point_diff' in enhanced_df.columns:
        enhanced_df['home_team_won'] = (enhanced_df['point_diff'] > 0).astype(int)
    
    # Extract day of week, month, year, and hour
    if 'date' in enhanced_df.columns and pd.api.types.is_datetime64_any_dtype(enhanced_df['date']):
        enhanced_df['day_of_week'] = enhanced_df['date'].dt.day_name()
        enhanced_df['month'] = enhanced_df['date'].dt.month_name()
        enhanced_df['year'] = enhanced_df['date'].dt.year
        enhanced_df['hour'] = enhanced_df['datetime'].dt.hour

    
    logger.info("Enhanced game DataFrame shape: %s", enhanced_df.shape)
    logger.info("Enhanced game DataFrame summary:\n%s", enhanced_df.describe())

    
    return enhanced_df

def prepare_home_vs_away(games_df):
    """
    Calculate aggregate team statistics from game data.
    
    Args:
        df (pandas.DataFrame): DataFrame containing game data
        
    Returns:
        pandas.DataFrame: Team statistics DataFrame
    """
    if games_df.empty:
        return pd.DataFrame()
    
    # Make sure the input DataFrame has the necessary columns
    required_columns = [
        'home_team_id', 'home_team_name', 'visitor_team_id', 
        'visitor_team_name', 'home_team_score', 'visitor_team_score', 
        'season'
    ]
    
    if not all(col in games_df.columns for col in required_columns):
        missing = [col for col in required_columns if col not in games_df.columns]
        raise ValueError(f"Missing required columns: {missing}")
    
    # Create home team records
    home_team_stats = games_df.rename(columns={
        'home_team_id': 'team_id',
        'home_team_name': 'team_name',
        'home_team_score': 'points_scored',
        'visitor_team_score': 'points_allowed',
    }).assign(
        is_home=True
    )
    
    # Create visitor team records
    visitor_team_stats = games_df.rename(columns={
        'visitor_team_id': 'team_id',
        'visitor_team_name': 'team_name',
        'visitor_team_score': 'points_scored',
        'home_team_score': 'points_allowed',
    }).assign(
        is_home=False
    )
    
    # Select common columns for both home and visitor records
    columns_to_keep = [
        'team_id', 'team_name', 'season', 'date', 
        'points_scored', 'points_allowed', 'is_home'
    ]
    
    # Ensure all columns exist in the dataframes
    home_columns = [col for col in columns_to_keep if col in home_team_stats.columns]
    visitor_columns = [col for col in columns_to_keep if col in visitor_team_stats.columns]
    
    # Combine home and visitor records
    combined_stats = pd.concat([
        home_team_stats[home_columns],
        visitor_team_stats[visitor_columns]
    ], ignore_index=True)
    
    # Calculate wins and point differential
    combined_stats['won'] = combined_stats['points_scored'] > combined_stats['points_allowed']
    combined_stats['point_diff'] = combined_stats['points_scored'] - combined_stats['points_allowed']
    
    # Group by team and season to calculate aggregated stats
    team_season_stats = combined_stats.groupby(['team_id', 'team_name', 'season']).agg(
        games_played=('team_id', 'count'),
        wins=('won', 'sum'),
        points_scored_total=('points_scored', 'sum'),
        points_allowed_total=('points_allowed', 'sum'),
        point_diff_total=('point_diff', 'sum'),
        point_diff_avg=('point_diff', 'mean'),
        home_games=('is_home', 'sum'),
        home_wins=('won', lambda x: (combined_stats.loc[x.index, 'is_home'] & 
                                    combined_stats.loc[x.index, 'won']).sum())
    ).reset_index()
    
    # Calculate additional metrics
    team_season_stats['losses'] = team_season_stats['games_played'] - team_season_stats['wins']
    team_season_stats['win_pct'] = team_season_stats['wins'] / team_season_stats['games_played']
    team_season_stats['points_per_game'] = team_season_stats['points_scored_total'] / team_season_stats['games_played']
    team_season_stats['points_allowed_per_game'] = team_season_stats['points_allowed_total'] / team_season_stats['games_played']
    
    # Calculate away games and wins
    team_season_stats['away_games'] = team_season_stats['games_played'] - team_season_stats['home_games']
    team_season_stats['away_wins'] = team_season_stats['wins'] - team_season_stats['home_wins']
    
    # Calculate home and away win percentages
    home_mask = team_season_stats['home_games'] > 0
    away_mask = team_season_stats['away_games'] > 0
    
    team_season_stats.loc[home_mask, 'home_win_pct'] = (
        team_season_stats.loc[home_mask, 'home_wins'] / team_season_stats.loc[home_mask, 'home_games']
    )
    
    team_season_stats.loc[away_mask, 'away_win_pct'] = (
        team_season_stats.loc[away_mask, 'away_wins'] / team_season_stats.loc[away_mask, 'away_games']
    )
    
    return team_season_stats