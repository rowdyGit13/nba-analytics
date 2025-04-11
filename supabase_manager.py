#!/usr/bin/env python
"""
Streamlined Supabase Migration Tool

This script provides a simplified approach to:
1. Migrate data from local storage to Supabase
2. Test Supabase connection
3. Export data to CSV files for offline use
"""

import os
import sys
import pandas as pd
import logging
import argparse
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Setup paths
BASE_DIR = Path(__file__).parent
FIXTURES_DIR = BASE_DIR / "fixtures"
CSV_DIR = BASE_DIR / "streamlit_app/data"
os.makedirs(FIXTURES_DIR, exist_ok=True)
os.makedirs(CSV_DIR, exist_ok=True)

# Load environment variables
load_dotenv()

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_supabase_client():
    """Initialize and return a Supabase client."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.error("Supabase credentials missing in environment variables")
        return None
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase client initialized successfully")
        return supabase
    except Exception as e:
        logger.error(f"Error initializing Supabase client: {e}")
        return None

def test_supabase_connection():
    """Test the Supabase connection and return status."""
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

def load_csv_data(csv_path):
    """Load data from a CSV file."""
    try:
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path)
        else:
            logger.error(f"CSV file not found: {csv_path}")
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error loading CSV: {e}")
        return pd.DataFrame()

def migrate_dataframe_to_supabase(df, table_name):
    """Migrate a dataframe to a Supabase table."""
    supabase = get_supabase_client()
    if not supabase or df.empty:
        return False
    
    try:
        # Convert dataframe to list of records
        records = df.to_dict(orient="records")
        
        # Delete existing data to avoid duplicates
        logger.info(f"Deleting existing data from {table_name}...")
        supabase.table(table_name).delete().execute()
        
        # Insert new data in batches to avoid payload size limits
        batch_size = 1000
        success = True
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            try:
                response = supabase.table(table_name).insert(batch).execute()
                logger.info(f"Inserted batch {i//batch_size + 1}/{(len(records)-1)//batch_size + 1} into {table_name}")
            except Exception as e:
                logger.error(f"Error inserting batch to {table_name}: {e}")
                success = False
        
        return success
    except Exception as e:
        logger.error(f"Error migrating data to {table_name}: {e}")
        return False

def migrate_all_data():
    """Migrate all data to Supabase from CSV files."""
    # Check connection first
    if not test_supabase_connection():
        logger.error("Supabase connection failed. Check your credentials.")
        return False
    
    # Table mapping
    tables = {
        "teams": "nba_data_team",
        "players": "nba_data_player",
        "games": "nba_data_game"
    }
    
    success = True
    for local_name, table_name in tables.items():
        csv_path = CSV_DIR / f"{local_name}.csv"
        df = load_csv_data(csv_path)
        
        if df.empty:
            logger.warning(f"No data found for {local_name}")
            success = False
            continue
        
        logger.info(f"Migrating {len(df)} {local_name} records to Supabase...")
        if not migrate_dataframe_to_supabase(df, table_name):
            success = False
    
    return success

def export_data_to_csv():
    """Export data from Supabase to CSV files."""
    supabase = get_supabase_client()
    if not supabase:
        return False
    
    # Table mapping
    tables = {
        "nba_data_team": "teams",
        "nba_data_player": "players",
        "nba_data_game": "games"
    }
    
    success = True
    for table_name, local_name in tables.items():
        try:
            response = supabase.table(table_name).select("*").execute()
            data = response.data
            
            if data:
                df = pd.DataFrame(data)
                csv_path = CSV_DIR / f"{local_name}.csv"
                df.to_csv(csv_path, index=False)
                logger.info(f"Exported {len(df)} records from {table_name} to {csv_path}")
            else:
                logger.warning(f"No data found in {table_name}")
                success = False
        except Exception as e:
            logger.error(f"Error exporting data from {table_name}: {e}")
            success = False
    
    return success

def main():
    """Main function with command-line arguments or interactive menu."""
    parser = argparse.ArgumentParser(description="NBA Analytics Dashboard - Supabase Data Manager")
    parser.add_argument("--test", action="store_true", help="Test Supabase connection")
    parser.add_argument("--migrate", action="store_true", help="Migrate data from CSV to Supabase")
    parser.add_argument("--export", action="store_true", help="Export data from Supabase to CSV")
    parser.add_argument("--quiet", action="store_true", help="Run in quiet mode (no interactive prompts)")
    
    args = parser.parse_args()
    
    # If command-line arguments are provided, run in non-interactive mode
    if args.test or args.migrate or args.export:
        results = []
        success = True
        
        if args.test:
            test_result = test_supabase_connection()
            results.append(("Test connection", test_result))
            success = success and test_result
        
        if args.migrate:
            migrate_result = migrate_all_data()
            results.append(("Migrate data", migrate_result))
            success = success and migrate_result
        
        if args.export:
            export_result = export_data_to_csv()
            results.append(("Export data", export_result))
            success = success and export_result
        
        # Print results unless quiet mode is enabled
        if not args.quiet:
            print("\n=== Results ===")
            for task, result in results:
                status = "✅ Success" if result else "❌ Failed"
                print(f"{task}: {status}")
        
        # Return exit code for scripting
        return 0 if success else 1
    
    # If no arguments provided, run in interactive mode
    print("=== NBA Analytics Dashboard - Supabase Data Manager ===")
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Test Supabase connection")
        print("2. Migrate data from CSV to Supabase")
        print("3. Export data from Supabase to CSV")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == "1":
            if test_supabase_connection():
                print("✅ Supabase connection successful!")
            else:
                print("❌ Supabase connection failed. Check your credentials.")
        
        elif choice == "2":
            if migrate_all_data():
                print("✅ Data migration to Supabase completed successfully!")
            else:
                print("❌ Some data failed to migrate. Check the logs for details.")
        
        elif choice == "3":
            if export_data_to_csv():
                print("✅ Data exported to CSV files successfully!")
            else:
                print("❌ Some data failed to export. Check the logs for details.")
        
        elif choice == "4":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    sys.exit(main())
