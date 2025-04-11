#!/bin/bash

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}==== NBA Analytics Dashboard - Supabase Setup ====${NC}"
echo "This script will help you set up your app with Supabase."
echo

# Check for required commands
command -v python3 >/dev/null 2>&1 || { 
    echo -e "${RED}Error: python3 is required but not installed.${NC}" 
    exit 1
}

# Always activate virtual environment - fail if not found
if [ -d "venv" ]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source venv/bin/activate
else
    echo -e "${RED}Error: Virtual environment (venv) not found.${NC}"
    echo "Please create a virtual environment with 'python3 -m venv venv' and install dependencies."
    exit 1
fi

# Verify that we're in the virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${RED}Error: Failed to activate virtual environment.${NC}"
    exit 1
else
    echo -e "${GREEN}Virtual environment activated: $(basename $VIRTUAL_ENV)${NC}"
fi

# Check if supabase package is installed
pip3 show supabase >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Installing Supabase Python package...${NC}"
    pip3 install supabase
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to install Supabase package.${NC}"
        exit 1
    fi
    echo -e "${GREEN}Supabase package installed successfully.${NC}"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found.${NC}"
    echo "Please create a .env file with your Supabase credentials."
    exit 1
fi

# Parse the .env file for Supabase credentials
echo -e "${YELLOW}Checking Supabase credentials in .env file...${NC}"
if grep -q "SUPABASE_URL" .env && grep -q "SUPABASE_KEY" .env; then
    echo -e "${GREEN}Supabase credentials found in .env file.${NC}"
    
    # Check if the credentials are placeholders
    if grep -q "yourdatabaseid" .env; then
        echo -e "${RED}Warning: Your Supabase credentials appear to be placeholders.${NC}"
        echo "Please update your .env file with your actual Supabase credentials."
    fi
else
    echo -e "${RED}Error: Supabase credentials not found in .env file.${NC}"
    echo "Please add SUPABASE_URL and SUPABASE_KEY to your .env file."
    exit 1
fi

# Menu
echo
echo -e "${YELLOW}What would you like to do?${NC}"
echo "1. Migrate data from local PostgreSQL to Supabase"
echo "2. Export data to CSV files for Streamlit Cloud deployment"
echo "3. Test database connection"
echo "4. Test Supabase direct access"
echo "5. Exit"
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo -e "${YELLOW}Running data migration script...${NC}"
        python3 migrate_to_supabase.py
        ;;
    2)
        echo -e "${YELLOW}Exporting data for Streamlit Cloud deployment...${NC}"
        python3 streamlit_app/export_data.py
        ;;
    3)
        echo -e "${YELLOW}Testing database connection...${NC}"
        python3 -c "
import os
import sys
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nba_analytics_project.settings')
django.setup()
from django.db import connections
cursor = connections['default'].cursor()
print('Database connection successful!')
"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Database connection successful!${NC}"
        else
            echo -e "${RED}Database connection failed. Check your credentials.${NC}"
        fi
        ;;
    4)
        echo -e "${YELLOW}Testing Supabase direct access...${NC}"
        python3 streamlit_app/supabase_client.py
        ;;
    5)
        echo -e "${YELLOW}Exiting setup script.${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac

echo
echo -e "${GREEN}Setup completed!${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Push your code to GitHub"
echo "2. Sign up for Streamlit Cloud (https://share.streamlit.io)"
echo "3. Connect your GitHub repository"
echo "4. Deploy your app!"
echo 