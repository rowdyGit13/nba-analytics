#!/usr/bin/env python3
"""
Script to check what tables exist in the Supabase database.
"""
import os
from dotenv import load_dotenv
from supabase import create_client
import pandas as pd

# Load environment variables
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def check_tables():
    """Check what tables exist in the Supabase database"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Supabase credentials not found in environment variables")
        return
    
    try:
        # Create Supabase client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Connected to Supabase successfully")
        
        # List all tables in the database
        print("\nAttempting to list tables...")
        
        # Method 1: Using information_schema
        try:
            response = supabase.table("information_schema.tables").select("table_schema,table_name").eq("table_schema", "public").execute()
            
            if response.data:
                print("\n=== Tables in the public schema ===")
                for table in response.data:
                    print(f"- {table['table_name']}")
            else:
                print("No tables found in the public schema using information_schema")
        except Exception as e:
            print(f"Error listing tables via information_schema: {e}")
        
        # Method 2: Try to list all users table
        print("\nAttempting to list specific tables by name...")
        tables_to_check = [
            "teams", "players", "games",
            "team", "player", "game",
            "nba_data_team", "nba_data_player", "nba_data_game"
        ]
        
        found_tables = []
        for table in tables_to_check:
            try:
                # Just try to select count to see if table exists
                response = supabase.table(table).select("count", count="exact").limit(1).execute()
                print(f"✅ '{table}' table exists. Count: {response.count}")
                found_tables.append(table)
            except Exception as e:
                error_msg = str(e)
                if "does not exist" in error_msg:
                    print(f"❌ '{table}' table does not exist")
                else:
                    print(f"❓ Error checking '{table}' table: {e}")
        
        # Summary
        print("\n=== Summary ===")
        if found_tables:
            print(f"Found {len(found_tables)} tables: {', '.join(found_tables)}")
            print("\nTo use these tables, update your code to reference the correct table names.")
        else:
            print("No tables found. You need to migrate your data to Supabase first.")
            print("\nTo migrate your data, run:")
            print("  source venv/bin/activate && python3 migrate_to_supabase.py")
    
    except Exception as e:
        print(f"❌ Error connecting to Supabase: {e}")

if __name__ == "__main__":
    print("Checking Supabase tables...")
    check_tables() 