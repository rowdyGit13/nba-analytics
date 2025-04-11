import subprocess
import os
import sys
import logging
from pathlib import Path
from django.core.management import call_command

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nba_analytics_project.settings')

# Django setup - add this to initialize Django if you don't use the manage.py command
import django
django.setup()

# Make sure the processed data directory exists
PROCESSED_DATA_DIR = Path(__file__).parent / "data" / "processed"
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Run the Streamlit app
if __name__ == "__main__":
    print("Starting NBA Analytics Dashboard...")
    
    # Run process_data.py to process data and export to CSV files
    print("Processing NBA data...")
    
    # Process current season data
    import datetime
    current_year = datetime.datetime.now().year
    
    # Process all data currently in the database and save dataframes as CSV files
    call_command('process_data', export=True, 
                export_dir=str(PROCESSED_DATA_DIR))
    print("✅ Processed all historical data")
    
    # Run the Streamlit app
    subprocess.run(["streamlit", "run", "streamlit_app/app.py"]) 