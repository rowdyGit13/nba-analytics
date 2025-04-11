"""
Data loader for the Streamlit app that handles multiple data sources:
1. Django ORM (primary)
2. Direct Supabase client (secondary)
3. CSV files (fallback)
"""

import os
import pandas as pd
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define data directory for CSV fallbacks
DATA_DIR = Path(__file__).parent / "data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_teams_dataframe():
    """
    Get teams dataframe with multiple fallback options:
    1. Django ORM
    2. Direct Supabase access
    3. CSV fallback
    """
    # Strategy 1: Try Django ORM first
    try:
        # First, try to load from database via Django ORM
        from nba_data.analytics.dataframes import get_teams_dataframe as get_db_teams
        teams_df = get_db_teams()
        
        # If we successfully loaded from database, cache to CSV for future fallback
        if not teams_df.empty:
            teams_df.to_csv(DATA_DIR / "teams.csv", index=False)
            logger.info("Retrieved teams data from Django ORM")
            return teams_df
    except Exception as e:
        logger.warning(f"Error connecting to database via Django ORM for teams: {e}")
    
    # Strategy 2: Try direct Supabase access
    try:
        from streamlit_app.supabase_client import get_teams_from_supabase
        teams_df = get_teams_from_supabase()
        
        # If we successfully loaded from Supabase, cache to CSV for future fallback
        if not teams_df.empty:
            teams_df.to_csv(DATA_DIR / "teams.csv", index=False)
            logger.info("Retrieved teams data directly from Supabase")
            return teams_df
    except Exception as e:
        logger.warning(f"Error connecting to Supabase for teams: {e}")
    
    # Strategy 3: Fallback to CSV
    try:
        if os.path.exists(DATA_DIR / "teams.csv"):
            logger.info("Loading teams from CSV fallback")
            return pd.read_csv(DATA_DIR / "teams.csv")
    except Exception as e:
        logger.error(f"Error loading teams CSV: {e}")
    
    # Return empty dataframe if all methods fail
    logger.error("All data retrieval methods failed for teams")
    return pd.DataFrame()

def get_players_dataframe():
    """
    Get players dataframe with multiple fallback options:
    1. Django ORM
    2. Direct Supabase access
    3. CSV fallback
    """
    # Strategy 1: Try Django ORM first
    try:
        # First, try to load from database via Django ORM
        from nba_data.analytics.dataframes import get_players_dataframe as get_db_players
        players_df = get_db_players()
        
        # If we successfully loaded from database, cache to CSV for future fallback
        if not players_df.empty:
            players_df.to_csv(DATA_DIR / "players.csv", index=False)
            logger.info("Retrieved players data from Django ORM")
            return players_df
    except Exception as e:
        logger.warning(f"Error connecting to database via Django ORM for players: {e}")
    
    # Strategy 2: Try direct Supabase access
    try:
        from streamlit_app.supabase_client import get_players_from_supabase
        players_df = get_players_from_supabase()
        
        # If we successfully loaded from Supabase, cache to CSV for future fallback
        if not players_df.empty:
            players_df.to_csv(DATA_DIR / "players.csv", index=False)
            logger.info("Retrieved players data directly from Supabase")
            return players_df
    except Exception as e:
        logger.warning(f"Error connecting to Supabase for players: {e}")
    
    # Strategy 3: Fallback to CSV
    try:
        if os.path.exists(DATA_DIR / "players.csv"):
            logger.info("Loading players from CSV fallback")
            return pd.read_csv(DATA_DIR / "players.csv")
    except Exception as e:
        logger.error(f"Error loading players CSV: {e}")
    
    # Return empty dataframe if all methods fail
    logger.error("All data retrieval methods failed for players")
    return pd.DataFrame()

def get_games_dataframe():
    """
    Get games dataframe with multiple fallback options:
    1. Django ORM
    2. Direct Supabase access
    3. CSV fallback
    """
    # Strategy 1: Try Django ORM first
    try:
        # First, try to load from database via Django ORM
        from nba_data.analytics.dataframes import get_games_dataframe as get_db_games
        games_df = get_db_games()
        
        # If we successfully loaded from database, cache to CSV for future fallback
        if not games_df.empty:
            games_df.to_csv(DATA_DIR / "games.csv", index=False)
            logger.info("Retrieved games data from Django ORM")
            return games_df
    except Exception as e:
        logger.warning(f"Error connecting to database via Django ORM for games: {e}")
    
    # Strategy 2: Try direct Supabase access
    try:
        from streamlit_app.supabase_client import get_games_from_supabase
        games_df = get_games_from_supabase()
        
        # If we successfully loaded from Supabase, cache to CSV for future fallback
        if not games_df.empty:
            games_df.to_csv(DATA_DIR / "games.csv", index=False)
            logger.info("Retrieved games data directly from Supabase")
            return games_df
    except Exception as e:
        logger.warning(f"Error connecting to Supabase for games: {e}")
    
    # Strategy 3: Fallback to CSV
    try:
        if os.path.exists(DATA_DIR / "games.csv"):
            logger.info("Loading games from CSV fallback")
            return pd.read_csv(DATA_DIR / "games.csv")
    except Exception as e:
        logger.error(f"Error loading games CSV: {e}")
    
    # Return empty dataframe if all methods fail
    logger.error("All data retrieval methods failed for games")
    return pd.DataFrame()

def export_all_dataframes():
    """
    Export all dataframes to CSV files for offline use.
    Try both Django ORM and direct Supabase access.
    """
    success = False
    
    # Try Django ORM first
    try:
        # Import directly from the Django module
        from nba_data.analytics.dataframes import (
            get_teams_dataframe as get_db_teams,
            get_players_dataframe as get_db_players,
            get_games_dataframe as get_db_games
        )
        
        # Get dataframes
        teams_df = get_db_teams()
        players_df = get_db_players()
        games_df = get_db_games()
        
        # Export to CSV
        if not teams_df.empty:
            teams_df.to_csv(DATA_DIR / "teams.csv", index=False)
            logger.info(f"Exported teams data from Django ORM: {len(teams_df)} records")
            success = True
        
        if not players_df.empty:
            players_df.to_csv(DATA_DIR / "players.csv", index=False)
            logger.info(f"Exported players data from Django ORM: {len(players_df)} records")
            success = True
        
        if not games_df.empty:
            games_df.to_csv(DATA_DIR / "games.csv", index=False)
            logger.info(f"Exported games data from Django ORM: {len(games_df)} records")
            success = True
            
    except Exception as e:
        logger.warning(f"Error exporting dataframes from Django ORM: {e}")
    
    # If Django ORM failed or data is incomplete, try Supabase
    if not success:
        try:
            # Import from Supabase client
            from streamlit_app.supabase_client import (
                get_teams_from_supabase,
                get_players_from_supabase,
                get_games_from_supabase
            )
            
            # Get dataframes from Supabase
            teams_df = get_teams_from_supabase()
            players_df = get_players_from_supabase()
            games_df = get_games_from_supabase()
            
            # Export to CSV
            if not teams_df.empty:
                teams_df.to_csv(DATA_DIR / "teams.csv", index=False)
                logger.info(f"Exported teams data from Supabase: {len(teams_df)} records")
                success = True
            
            if not players_df.empty:
                players_df.to_csv(DATA_DIR / "players.csv", index=False)
                logger.info(f"Exported players data from Supabase: {len(players_df)} records")
                success = True
            
            if not games_df.empty:
                games_df.to_csv(DATA_DIR / "games.csv", index=False)
                logger.info(f"Exported games data from Supabase: {len(games_df)} records")
                success = True
                
        except Exception as e:
            logger.error(f"Error exporting dataframes from Supabase: {e}")
    
    return success

# If this script is run directly, export the data
if __name__ == "__main__":
    print("Exporting dataframes to CSV files...")
    if export_all_dataframes():
        print("✅ Export successful!")
    else:
        print("❌ Export failed. Check the logs for details.") 