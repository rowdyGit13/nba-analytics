#!/usr/bin/env python3
"""
Test script to verify Supabase connectivity.
Usage: python3 test_supabase.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def test_supabase_connection():
    """Test connection to Supabase"""
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: Supabase credentials not found in environment variables.")
        print("Make sure SUPABASE_URL and SUPABASE_KEY are set in your .env file.")
        return False
    
    try:
        from supabase import create_client
        
        # Initialize the Supabase client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Try a simple query to check connectivity
        response = supabase.table("nba_data_team").select("count", count="exact").execute()
        
        # Print the results
        print(f"✅ Successfully connected to Supabase!")
        print(f"URL: {SUPABASE_URL}")
        print(f"Tables available: nba_data_team")
        print(f"Total teams count: {response.count if hasattr(response, 'count') else 'unknown'}")
        
        return True
    except ImportError:
        print("❌ Error: Supabase package not installed.")
        print("Run: pip install supabase")
        return False
    except Exception as e:
        print(f"❌ Error connecting to Supabase: {e}")
        print("Check your credentials and try again.")
        return False

def main():
    """Main function"""
    print("Testing Supabase connectivity...")
    success = test_supabase_connection()
    
    if success:
        print("\nNext steps:")
        print("1. Run 'bash setup_supabase.sh' to continue setup")
        print("2. Choose option 1 to migrate data from local database to Supabase")
        print("3. Or choose option 2 to export data to CSV files")
    else:
        print("\nPlease fix the issues above and try again.")

if __name__ == "__main__":
    main() 