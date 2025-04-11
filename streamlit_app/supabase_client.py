"""
Supabase client utility for direct access to Supabase from the Streamlit app.
This is an alternative method to access data directly from Supabase
without going through Django models.
"""

import os
import logging
from dotenv import load_dotenv
from pathlib import Path
from supabase import create_client
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_supabase_client():
    """
    Initialize and return a Supabase client.
    
    Returns:
        Supabase client if credentials are valid, None otherwise
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.error("Supabase credentials missing in environment variables")
        return None
    
    try:
        # Create Supabase client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase client initialized successfully")
        return supabase
    except Exception as e:
        logger.error(f"Error initializing Supabase client: {e}")
        return None

def test_supabase_connection():
    """
    Test the connection to Supabase.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    supabase = get_supabase_client()
    if not supabase:
        return False
    
    try:
        # Simple query to test connection
        response = supabase.table("nba_data_team").select("id").limit(1).execute()
        logger.info("Supabase connection test successful")
        return True
    except Exception as e:
        logger.error(f"Supabase connection test failed: {e}")
        return False

def get_teams_from_supabase():
    """
    Get teams data directly from Supabase.
    
    Returns:
        pandas.DataFrame: DataFrame with teams data or empty DataFrame if failed
    """
    supabase = get_supabase_client()
    if not supabase:
        return pd.DataFrame()
    
    try:
        # Query the teams table
        response = supabase.table('nba_data_team').select('*').execute()
        data = response.data
        
        if data:
            return pd.DataFrame(data)
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error fetching teams from Supabase: {e}")
        return pd.DataFrame()

def get_players_from_supabase():
    """
    Get players data directly from Supabase.
    
    Returns:
        pandas.DataFrame: DataFrame with players data or empty DataFrame if failed
    """
    supabase = get_supabase_client()
    if not supabase:
        return pd.DataFrame()
    
    try:
        # Query the players table
        response = supabase.table('nba_data_player').select('*').execute()
        data = response.data
        
        if data:
            return pd.DataFrame(data)
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error fetching players from Supabase: {e}")
        return pd.DataFrame()

def get_games_from_supabase():
    """
    Get games data directly from Supabase.
    
    Returns:
        pandas.DataFrame: DataFrame with games data or empty DataFrame if failed
    """
    supabase = get_supabase_client()
    if not supabase:
        return pd.DataFrame()
    
    try:
        # Query the games table
        response = supabase.table('nba_data_game').select('*').execute()
        data = response.data
        
        if data:
            return pd.DataFrame(data)
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error fetching games from Supabase: {e}")
        return pd.DataFrame()

# Example usage if this script is run directly
if __name__ == "__main__":
    print("Testing Supabase connection...")
    
    if test_supabase_connection():
        print("✅ Supabase connection successful!")
        
        # Test fetching teams
        teams_df = get_teams_from_supabase()
        if not teams_df.empty:
            print(f"Found {len(teams_df)} teams in Supabase")
        else:
            print("No teams found in Supabase")
    else:
        print("❌ Failed to connect to Supabase")
        print("Check your credentials and try again") 