#!/usr/bin/env python3
"""
Debug script for Supabase API key issues.
This script helps identify common problems with Supabase API keys.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("=== Supabase API Key Debugger ===")
print("\nChecking configuration...")

# Check if values exist
if not SUPABASE_URL:
    print("❌ SUPABASE_URL is missing or empty in .env file")
else:
    # Remove quotes if present
    SUPABASE_URL = SUPABASE_URL.strip('"').strip("'")
    print(f"✅ SUPABASE_URL found: {SUPABASE_URL}")
    
    # Check URL format
    if not SUPABASE_URL.startswith("https://"):
        print("❌ SUPABASE_URL should start with 'https://'")
    if not SUPABASE_URL.endswith(".supabase.co"):
        print("❌ SUPABASE_URL should end with '.supabase.co'")

if not SUPABASE_KEY:
    print("❌ SUPABASE_KEY is missing or empty in .env file")
else:
    # Remove quotes if present
    SUPABASE_KEY = SUPABASE_KEY.strip('"').strip("'")
    
    # Check for common problems
    if "postgresql://" in SUPABASE_KEY:
        print("❌ ERROR: You've provided a PostgreSQL connection string instead of an API key")
        print("   The SUPABASE_KEY should be the 'anon' or 'service_role' key from your Supabase project")
        print("   Go to your Supabase dashboard → Project Settings → API → Project API Keys")
        print("   Use either the 'anon' key (for public access) or 'service_role' key (for admin access)\n")
        
        # Try to extract project ref
        project_ref = None
        if "db." in SUPABASE_KEY and ".supabase.co" in SUPABASE_KEY:
            parts = SUPABASE_KEY.split("db.")[1].split(".supabase.co")[0]
            project_ref = parts
            print(f"ℹ️ Your project reference appears to be: {project_ref}")
            print("   Use this to find your project in the Supabase dashboard")
    elif len(SUPABASE_KEY) < 30:
        print("❌ SUPABASE_KEY looks too short. Should be a long API key")
    else:
        print(f"✅ SUPABASE_KEY found (length: {len(SUPABASE_KEY)} characters)")
        
        # Check if it's a JWT token
        if SUPABASE_KEY.count('.') == 2 and SUPABASE_KEY.startswith("ey"):
            print("ℹ️ Your key appears to be a JWT token, which is likely correct")
        
print("\n=== Steps to find your Supabase API key ===")
print("1. Go to https://app.supabase.com/")
print("2. Select your project")
print("3. Go to Project Settings (gear icon) → API")
print("4. Copy the 'anon' key (for public access) or 'service_role' key (for admin access)")
print("5. Update your .env file with the correct key:")
print("   SUPABASE_URL = \"https://your-project-ref.supabase.co\"")
print("   SUPABASE_KEY = \"your-api-key-here\"")
print("\nNote: Don't use quotes in .env values unless needed for special characters") 