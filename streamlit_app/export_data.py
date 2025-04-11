#!/usr/bin/env python
"""
Script to export the database data to CSV files for use in Streamlit Cloud.
Run this before deploying to Streamlit Cloud to ensure data is available.
"""

import os
import sys
import django
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nba_analytics_project.settings')
django.setup()

# Import the data loader
from streamlit_app.data_loader import export_all_dataframes

if __name__ == "__main__":
    print("Exporting data for Streamlit Cloud deployment...")
    if export_all_dataframes():
        print("✅ Data export successful!")
        print("Your app is now ready for Streamlit Cloud deployment.")
    else:
        print("❌ Data export failed.")
        print("Check your database connection and try again.") 