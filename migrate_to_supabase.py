#!/usr/bin/env python
"""
Script to migrate data from local PostgreSQL to Supabase PostgreSQL.
This script should be run after setting up your Supabase credentials in .env.

Usage:
  1. Activate your virtual environment
  2. Run: python3 migrate_to_supabase.py
"""

import os
import sys
import django
from django.core.management import call_command
import subprocess
from dotenv import load_dotenv
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nba_analytics_project.settings')
django.setup()

# Load environment variables
load_dotenv()

# Create a .local_env file if you want to override local database settings
local_env_path = Path('.local_env')
if local_env_path.exists():
    load_dotenv(dotenv_path=local_env_path)

def backup_local_data():
    """Create a database dump from the local PostgreSQL database"""
    print("Backing up local data...")
    
    # Try to get local database settings from .local_env file first, then fall back to defaults
    db_name = os.getenv('LOCAL_DB_NAME', 'testdb')  # Local DB name
    db_user = os.getenv('LOCAL_DB_USER', 'nba_superuser')  # Local DB user
    db_password = os.getenv('LOCAL_DB_PASSWORD', '')  # Local DB password (if required)
    
    print(f"Using local database: {db_name} with user: {db_user}")
    
    # Ask user to confirm settings
    confirm = input("Are these settings correct? (y/n): ")
    if confirm.lower() != 'y':
        db_name = input("Enter local database name: ")
        db_user = input("Enter local database username: ")
        # Password will be requested by pg_dump if needed
    
    # Create backup directory if it doesn't exist
    if not os.path.exists('backup'):
        os.makedirs('backup')
    
    # Dump the database to a file
    backup_path = os.path.join('backup', 'local_db_dump.sql')
    pg_dump_cmd = f"pg_dump -U {db_user} -d {db_name} -f {backup_path}"
    
    try:
        subprocess.run(pg_dump_cmd, shell=True, check=True)
        print(f"Database backup created at {backup_path}")
        return backup_path
    except subprocess.CalledProcessError as e:
        print(f"Error creating database backup: {e}")
        return None

def migrate_to_supabase(backup_path):
    """Restore the backup to the Supabase PostgreSQL database"""
    print("Migrating data to Supabase...")
    
    # Get Supabase database settings
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    
    print(f"Will connect to Supabase at: {db_host} as user: {db_user}")
    confirm = input("Continue with migration? (y/n): ")
    if confirm.lower() != 'y':
        print("Migration cancelled")
        return
    
    # Set PGPASSWORD environment variable for psql
    os.environ['PGPASSWORD'] = db_password
    
    # Restore the database
    psql_cmd = f"psql -h {db_host} -p {db_port} -U {db_user} -d {db_name} -f {backup_path}"
    
    try:
        subprocess.run(psql_cmd, shell=True, check=True)
        print("Database migration to Supabase completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error migrating database to Supabase: {e}")

def django_migration_approach():
    """Alternative approach using Django's dumpdata and loaddata commands"""
    print("Using Django migration approach...")
    
    # Create fixtures directory if it doesn't exist
    if not os.path.exists('fixtures'):
        os.makedirs('fixtures')
    
    print("Dumping data from local database...")
    # Dump data from Django models
    call_command('dumpdata', 'nba_data', output='fixtures/nba_data.json', indent=2)
    
    print("Checking if dump was successful...")
    if not os.path.exists('fixtures/nba_data.json'):
        print("Error: Data dump failed. Check your local database connection.")
        return
    
    print("Data dump successful.")
    print("Size of data dump: ", os.path.getsize('fixtures/nba_data.json'), "bytes")
    
    # Now we need to update the DATABASE settings to point to Supabase
    print("\nNow connecting to Supabase database...")
    print("Will apply migrations and load data into Supabase")
    
    confirm = input("Continue with migration to Supabase? (y/n): ")
    if confirm.lower() != 'y':
        print("Migration cancelled")
        return
    
    # Apply migrations to the Supabase database
    print("Applying migrations...")
    call_command('migrate')
    
    # Load data into Supabase
    print("Loading data...")
    call_command('loaddata', 'fixtures/nba_data.json')
    
    print("Django migration to Supabase completed successfully!")

def main():
    """Main function to coordinate the migration process"""
    print("=== NBA Data Migration to Supabase ===")
    print("This script will migrate your local database to Supabase.")
    
    choice = input("""
Choose migration method:
1. PostgreSQL dump/restore (requires pg_dump and psql installed)
2. Django dumpdata/loaddata (pure Python, recommended for most users)
Choice (1/2): """)
    
    if choice == '1':
        backup_path = backup_local_data()
        if backup_path:
            migrate_to_supabase(backup_path)
    elif choice == '2':
        django_migration_approach()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main() 