import pandas as pd
import os
import sys
import logging
from pathlib import Path
import importlib.util

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global variables to store DataFrames
cleaned_players_df = pd.DataFrame()
cleaned_teams_df = pd.DataFrame()
prepared_games_df = pd.DataFrame()
team_metrics_df = pd.DataFrame()
team_rankings_df = pd.DataFrame()

def is_django_available():
    """Check if Django settings module is available"""
    django_settings_spec = importlib.util.find_spec('nba_analytics_project.settings')
    return django_settings_spec is not None

def setup_django():
    """Set up Django environment if not already set up"""
    if not is_django_available():
        logger.warning("Django settings module not found, skipping Django setup")
        return False
        
    if 'DJANGO_SETTINGS_MODULE' not in os.environ:
        # Add the parent directory to sys.path
        parent_dir = str(Path(__file__).resolve().parent.parent.parent)
        if parent_dir not in sys.path:
            sys.path.append(parent_dir)
        
        # Set up Django environment
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nba_analytics_project.settings')
        try:
            import django
            django.setup()
            return True
        except ImportError:
            logger.warning("Django module not found, skipping Django setup")
            return False
    return True

def load_data_from_django():
    """Load data directly from Django models using the process_data logic"""
    global cleaned_players_df, cleaned_teams_df, prepared_games_df, team_metrics_df, team_rankings_df
    
    try:
        # Set up Django environment
        if not setup_django():
            logger.warning("Django setup failed. Skipping Django data load.")
            return False
        
        # Import necessary modules
        try:
            from nba_data.analytics import dataframes, data_prep, stats
        except ImportError as e:
            logger.error(f"Could not import Django modules: {e}")
            return False
        
        logger.info("Loading data from Django models...")
        
        # Load data from database
        teams_df = dataframes.get_teams_dataframe()
        if teams_df.empty:
            logger.warning('No teams found in database.')
            return False
        
        players_df = dataframes.get_players_dataframe()
        if players_df.empty:
            logger.warning('No players found in database.')
            return False
        
        games_df = dataframes.get_games_dataframe()
        if games_df.empty:
            logger.warning('No games found in database.')
            return False
        
        # Clean and transform data
        cleaned_players_df = data_prep.clean_player_data(players_df)
        cleaned_teams_df = data_prep.clean_teams_data(teams_df)
        cleaned_games_df = data_prep.clean_games_data(games_df)
        
        # Calculate team statistics
        prepared_games_df = data_prep.enhance_game_data(cleaned_games_df)
        team_stats_df = data_prep.prepare_home_vs_away(prepared_games_df)
        
        if not team_stats_df.empty:
            team_metrics_df = stats.calculate_team_performance_metrics(team_stats_df)
            team_rankings_df = stats.calculate_team_rankings(team_metrics_df)
        
        logger.info("Successfully loaded data from Django models")
        return True
    
    except Exception as e:
        logger.error(f"Error loading data from Django models: {str(e)}", exc_info=True)
        return False

def load_data_from_csv():
    """Load data from CSV files as a backup"""
    global cleaned_players_df, cleaned_teams_df, prepared_games_df, team_metrics_df, team_rankings_df
    
    try:
        # Define paths - check multiple possible locations
        possible_data_dirs = [
            Path(__file__).parent.parent / "data" / "processed",  # streamlit_app/data/processed
            Path(__file__).parent.parent / "data",                # streamlit_app/data
            Path(__file__).resolve().parent.parent / "data" / "processed",
            Path.cwd() / "streamlit_app" / "data" / "processed",
            Path.cwd() / "data" / "processed",
        ]
        
        data_dir = None
        # Find first valid data directory
        for dir_path in possible_data_dirs:
            if dir_path.exists():
                data_dir = dir_path
                logger.info(f"Found data directory at {data_dir}")
                break
        
        if data_dir is None:
            logger.error("No valid data directory found")
            return False
        
        # Load DataFrames from CSV files
        logger.info(f"Loading data from CSV files in {data_dir}...")
        
        # Helper function to load a CSV file
        def load_csv_dataframe(filename):
            filepath = data_dir / filename
            if os.path.exists(filepath):
                try:
                    df = pd.read_csv(filepath)
                    logger.info(f"Loaded {filename} with {len(df)} records")
                    return df
                except Exception as e:
                    logger.error(f"Error loading {filename}: {e}")
                    return pd.DataFrame()
            else:
                logger.warning(f"File not found: {filepath}")
                return pd.DataFrame()
        
        # Load all required dataframes
        cleaned_players_df = load_csv_dataframe("players.csv")
        cleaned_teams_df = load_csv_dataframe("teams.csv")
        prepared_games_df = load_csv_dataframe("games.csv")
        team_metrics_df = load_csv_dataframe("team_metrics.csv")
        team_rankings_df = load_csv_dataframe("team_rankings.csv")
        
        # Check if we have at least some data
        if (not cleaned_teams_df.empty and 
            not cleaned_players_df.empty and 
            not prepared_games_df.empty):
            logger.info("Successfully loaded data from CSV files")
            return True
        else:
            logger.warning("One or more required DataFrames are empty")
            return False
    
    except Exception as e:
        logger.error(f"Error loading data from CSV files: {str(e)}", exc_info=True)
        return False

def get_data():
    """Get all DataFrames. Try to load from CSV first in standalone mode, Django in integrated mode"""
    # Check if running in standalone mode
    standalone_mode = not is_django_available()
    
    if standalone_mode:
        # In standalone mode, try CSV files first
        logger.info("Running in standalone mode, loading from CSV files...")
        if not load_data_from_csv():
            logger.error("Failed to load data from CSV files in standalone mode")
    else:
        # In integrated mode, try Django first
        logger.info("Running in integrated mode with Django")
        if not load_data_from_django():
            # If Django loading fails, try CSV files
            logger.info("Falling back to CSV data...")
            if not load_data_from_csv():
                logger.error("Failed to load data from both Django and CSV files")
    
    # Return DataFrames
    return {
        'players_df': cleaned_players_df,
        'teams_df': cleaned_teams_df,
        'games_df': prepared_games_df,
        'team_metrics_df': team_metrics_df,
        'team_rankings_df': team_rankings_df
    } 