import subprocess
import os
import sys
import django
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nba_analytics_project.settings')
django.setup()

def ensure_fresh_data():
    """Ensure fresh data is available to the Streamlit app"""
    try:
        # Try loading fresh data from Supabase
        from streamlit_app.supabase_client import test_supabase_connection
        
        if test_supabase_connection():
            # If Supabase connection works, export data to CSV as fallback
            logger.info("Supabase connection successful - exporting fresh data")
            from streamlit_app.data_loader import export_all_dataframes
            export_all_dataframes()
        else:
            logger.warning("Supabase connection failed - will use local data if available")
    except Exception as e:
        logger.error(f"Error ensuring fresh data: {e}")
        logger.info("Will use locally cached data if available")

# Run the Streamlit app
if __name__ == "__main__":
    print("Starting NBA Analytics Dashboard...")
    
    # Ensure fresh data is available
    ensure_fresh_data()
    
    # Run the Streamlit app
    subprocess.run(["streamlit", "run", "streamlit_app/app.py"]) 