"""
Module for statistical computations on NBA data.
These functions perform various statistical analyses using NumPy.
"""

import pandas as pd
import numpy as np

def calculate_team_performance_metrics(team_stats_df):
    """
    Calculate advanced team performance metrics.
    
    Args:
        team_stats_df (pandas.DataFrame): DataFrame containing team statistics
        
    Returns:
        pandas.DataFrame: Enhanced DataFrame with additional performance metrics
    """
    if team_stats_df.empty:
        return team_stats_df
    
    # Make a copy to avoid modifying the original
    df = team_stats_df.copy()
    
    # Offensive and defensive ratings (points per 100 possessions)
    # Note: This is a simplified calculation without possessions
    if all(col in df.columns for col in ['points_per_game', 'points_allowed_per_game']):
        df['offensive_rating'] = df['points_per_game'] * 100 / 100  # Simplified
        df['defensive_rating'] = df['points_allowed_per_game'] * 100 / 100  # Simplified
        df['net_rating'] = df['offensive_rating'] - df['defensive_rating']
    
    # Team rankings
    if 'win_pct' in df.columns:
        # Rank teams by win percentage within each season
        df['win_pct_rank'] = df.groupby('season')['win_pct'].rank(ascending=False)
    
    if 'points_per_game' in df.columns:
        # Offensive rankings
        df['offensive_rank'] = df.groupby('season')['points_per_game'].rank(ascending=False)
        
    if 'points_allowed_per_game' in df.columns:
        # Defensive rankings (lower points allowed is better)
        df['defensive_rank'] = df.groupby('season')['points_allowed_per_game'].rank(ascending=True)
    
    if 'point_diff_avg' in df.columns:
        # Net rating rank
        df['point_diff_rank'] = df.groupby('season')['point_diff_avg'].rank(ascending=False)
    
    # Calculate z-scores for various metrics (standardized scores)
    for metric in ['win_pct', 'points_per_game', 'points_allowed_per_game', 'point_diff_avg']:
        if metric in df.columns:
            z_col = f'{metric}_z'
            df[z_col] = df.groupby('season')[metric].transform(
                lambda x: (x - x.mean()) / x.std(ddof=0) if len(x) > 1 and x.std() > 0 else 0
            )
    
    return df

def calculate_team_rankings(team_stats_df, season=None):
    """
    Calculate team rankings for various metrics.
    
    Args:
        team_stats_df (pandas.DataFrame): DataFrame containing team statistics
        season (str, optional): Season to filter by in YYYY-YYYY format (e.g., '2022-2023')
        
    Returns:
        pandas.DataFrame: DataFrame with team rankings
    """
    if team_stats_df.empty:
        return pd.DataFrame()
    
    # Filter by season if provided
    df = team_stats_df.copy()
    if season is not None:
        df = df[df['season'] == season]
    
    if df.empty:
        return pd.DataFrame()
    
    # Select relevant columns for ranking
    ranking_cols = [
        'team_id', 'team_abbreviation', 'season',
        'win_pct', 'points_per_game', 'points_allowed_per_game', 'point_diff_avg'
    ]
    
    available_cols = [col for col in ranking_cols if col in df.columns]
    if len(available_cols) < 4:  # Need at least team identifier, season, and some metrics
        return pd.DataFrame()
    
    rankings = df[available_cols].copy()
    
    # Create rankings for each metric
    metric_cols = [
        ('win_pct', True, 'wins_rank'),
        ('points_per_game', True, 'offense_rank'),
        ('points_allowed_per_game', False, 'defense_rank'),
        ('point_diff_avg', True, 'diff_rank')
    ]
    
    for source_col, ascending_order, rank_col in metric_cols:
        if source_col in rankings.columns:
            rankings[rank_col] = rankings.groupby('season')[source_col].rank(
                ascending=not ascending_order, method='min'
            )
    
    # Calculate overall rank based on available metrics
    rank_cols = [col for _, _, col in metric_cols if col in rankings.columns]
    if rank_cols:
        rankings['overall_rank'] = rankings[rank_cols].mean(axis=1)
        rankings['overall_rank'] = rankings.groupby('season')['overall_rank'].rank(method='min')
    
    return rankings

def calculate_league_averages(games_df, team_stats_df=None):
    """
    Calculate league-wide averages for various metrics.
    
    Args:
        games_df (pandas.DataFrame): DataFrame containing game data
        team_stats_df (pandas.DataFrame, optional): DataFrame containing team statistics
        
    Returns:
        dict: Dictionary with league averages
    """
    league_averages = {}
    
    if games_df.empty:
        return league_averages
    
    # Calculate league-wide scoring averages from games
    if all(col in games_df.columns for col in ['home_team_score', 'visitor_team_score', 'season']):
        # Points per game
        games_df['total_points'] = games_df['home_team_score'] + games_df['visitor_team_score']
        games_df['avg_points_per_team'] = games_df['total_points'] / 2
        
        # League averages by season
        league_by_season = games_df.groupby('season').agg(
            avg_team_score=('avg_points_per_team', 'mean'),
            avg_game_total=('total_points', 'mean'),
            games_played=('game_id', 'count')
        ).reset_index()
        
        # Format as dictionary
        for _, row in league_by_season.iterrows():
            season = row['season']
            league_averages[season] = {
                'avg_team_score': row['avg_team_score'],
                'avg_game_total': row['avg_game_total'],
                'games_played': row['games_played']
            }
    
    # Add team statistics if provided
    if team_stats_df is not None and not team_stats_df.empty:
        for season in league_averages.keys():
            season_teams = team_stats_df[team_stats_df['season'] == season]
            
            # Only process if we have team data for this season
            if not season_teams.empty:
                # Home vs Away win percentages
                if 'home_win_pct' in season_teams.columns:
                    league_averages[season]['avg_home_win_pct'] = season_teams['home_win_pct'].mean()
                
                if 'away_win_pct' in season_teams.columns:
                    league_averages[season]['avg_away_win_pct'] = season_teams['away_win_pct'].mean()
                
                # Win percentage distribution
                if 'win_pct' in season_teams.columns:
                    league_averages[season]['win_pct_std'] = season_teams['win_pct'].std()
                    league_averages[season]['win_pct_25th'] = season_teams['win_pct'].quantile(0.25)
                    league_averages[season]['win_pct_median'] = season_teams['win_pct'].median()
                    league_averages[season]['win_pct_75th'] = season_teams['win_pct'].quantile(0.75)
    
    return league_averages