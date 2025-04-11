#!/usr/bin/env python
"""
Weekly NBA data update script

This script automates the weekly process of:
1. Importing teams, players, and games from the NBA API to the local database
2. Migrating this data to Supabase for the Streamlit app to access
3. Processing the data and generating analytics

Usage:
  python weekly_update.py [--no-import] [--no-migrate] [--no-process]
"""

import os
import sys
import argparse
import logging
import subprocess
from datetime import datetime
import django

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('update.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nba_analytics_project.settings')

def run_command(command, desc=None):
    """Run a shell command and log the output."""
    if desc:
        logger.info(f"Starting: {desc}")
    else:
        logger.info(f"Running command: {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        logger.info(f"Command succeeded: {command}")
        logger.debug(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {command}")
        logger.error(f"Error: {e}")
        logger.error(f"Output: {e.stdout}")
        logger.error(f"Error output: {e.stderr}")
        return False

def import_data(args):
    """Import data from the NBA API."""
    logger.info("Starting data import process...")
    
    # Import teams (always needed as a foundation)
    success = run_command(
        "python manage.py import_teams",
        "Importing NBA teams"
    )
    if not success:
        logger.error("Team import failed. Aborting import process.")
        return False
    
    # Import players
    success = run_command(
        "python manage.py import_players",
        "Importing NBA players"
    )
    if not success:
        logger.warning("Player import failed but continuing with games import.")
    
    # Import games for the current year
    current_year = datetime.now().year
    # Import both current year and previous year to ensure full season
    years_to_import = [current_year, current_year - 1]
    
    for year in years_to_import:
        success = run_command(
            f"python manage.py import_games --seasons {year}",
            f"Importing NBA games for {year}"
        )
        if not success:
            logger.warning(f"Games import for {year} failed.")
    
    logger.info("Data import process completed.")
    return True

def migrate_data(args):
    """Migrate data to Supabase."""
    logger.info("Starting data migration to Supabase...")
    
    # First, export data to CSV files for the Streamlit app's data folder
    success = run_command(
        "python streamlit_app/data_loader.py",
        "Exporting Django data to CSV files"
    )
    if not success:
        logger.warning("CSV export failed. Will try direct Supabase migration.")
    
    # Then migrate to Supabase
    success = run_command(
        "python supabase_manager.py --migrate --test",
        "Migrating data to Supabase"
    )
    if not success:
        logger.error("Supabase migration failed.")
        return False
    
    # Also export data from Supabase back to CSV as a backup and for offline use
    run_command(
        "python supabase_manager.py --export --quiet",
        "Exporting data from Supabase to CSV"
    )
    
    logger.info("Data migration process completed.")
    return True

def process_data(args):
    """Process data for analytics."""
    logger.info("Starting data processing for analytics...")
    
    # Get current year for analytics processing
    current_year = datetime.now().year
    
    # Process data for current season
    success = run_command(
        f"python manage.py process_data --season {current_year} --export --export-dir streamlit_app/data/processed",
        f"Processing NBA data for {current_year} season"
    )
    if not success:
        logger.warning(f"Data processing for {current_year} failed. Trying without season filter.")
        
        # Try processing without season filter as a fallback
        success = run_command(
            "python manage.py process_data --export --export-dir streamlit_app/data/processed",
            "Processing all NBA data"
        )
        if not success:
            logger.error("Data processing failed completely.")
            return False
    
    logger.info("Data processing completed.")
    return True

def main():
    """Main function handling the data flow."""
    parser = argparse.ArgumentParser(description="Weekly NBA data update script")
    parser.add_argument("--no-import", action="store_true", help="Skip importing from API")
    parser.add_argument("--no-migrate", action="store_true", help="Skip migrating to Supabase")
    parser.add_argument("--no-process", action="store_true", help="Skip data processing")
    
    args = parser.parse_args()
    
    logger.info(f"Starting weekly update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = True
    
    # Step 1: Import data from API
    if not args.no_import:
        if not import_data(args):
            logger.warning("Data import step had issues, but continuing with migration...")
    else:
        logger.info("Skipping data import (--no-import flag used)")
    
    # Step 2: Migrate data to Supabase
    if not args.no_migrate:
        if not migrate_data(args):
            logger.warning("Data migration step had issues, but continuing with processing...")
            success = False
    else:
        logger.info("Skipping data migration (--no-migrate flag used)")
    
    # Step 3: Process data for analytics
    if not args.no_process:
        if not process_data(args):
            logger.warning("Data processing step had issues.")
            success = False
    else:
        logger.info("Skipping data processing (--no-process flag used)")
    
    # Final status
    if success:
        logger.info("Weekly update completed successfully!")
        return 0
    else:
        logger.warning("Weekly update completed with some issues. Check the logs for details.")
        return 1

if __name__ == "__main__":
    try:
        # Setup Django environment
        django.setup()
        # Run the main function
        sys.exit(main())
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}", exc_info=True)
        sys.exit(1)
