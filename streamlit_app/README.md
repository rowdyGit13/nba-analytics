# NBA Analytics Dashboard - Streamlit Cloud Deployment

This guide provides instructions for deploying the NBA Analytics Dashboard to Streamlit Cloud.

## Setup Instructions

### Prerequisites
- GitHub account
- Streamlit Cloud account (sign up at https://share.streamlit.io)
- Supabase account and project (or exported CSV data)

### Option 1: Deploy with Supabase Database Connection

1. **Update .env file with your Supabase credentials**:
   ```
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=your_supabase_db_password
   DB_HOST=db.yourdatabaseid.supabase.co
   DB_PORT=5432
   SUPABASE_URL=https://yourdatabaseid.supabase.co
   SUPABASE_KEY=your_supabase_api_key
   ```

2. **Migrate your data to Supabase**:
   ```bash
   # Activate virtual environment
   source venv/bin/activate
   
   # Run the setup script
   bash setup_supabase.sh
   ```

3. **Push your code to GitHub**:
   - Create a new repository on GitHub
   - Push your code to the repository

4. **Deploy to Streamlit Cloud**:
   - Sign in to Streamlit Cloud
   - Connect your GitHub repository
   - Set up the following:
     - Main file path: `streamlit_app/app.py`
     - Python version: 3.11
     - Environment variables (add your Supabase credentials from .env)

### Option 2: Deploy with CSV Data (Simpler)

1. **Export your data to CSV files**:
   ```bash
   # Activate virtual environment
   source venv/bin/activate
   
   # Export data to CSV
   python streamlit_app/export_data.py
   ```

2. **Push your code to GitHub**:
   - Make sure to include the `streamlit_app/data` directory with the CSV files
   - Create a new repository on GitHub
   - Push your code to the repository

3. **Deploy to Streamlit Cloud**:
   - Sign in to Streamlit Cloud
   - Connect your GitHub repository
   - Set the main file path to `streamlit_app/app.py`
   - No additional environment variables needed

## Advanced Deployment Options

### Secrets Management
For better security, use Streamlit's secrets management:

1. Create a `.streamlit/secrets.toml` file:
   ```toml
   [postgres]
   host = "db.yourdatabaseid.supabase.co"
   port = 5432
   dbname = "postgres"
   user = "postgres"
   password = "your_supabase_password"
   ```

2. Update the app to use these secrets:
   ```python
   import streamlit as st
   # Use st.secrets["postgres"]["password"] instead of os.environ
   ```

### Custom Domain
Streamlit Cloud allows you to set up a custom domain for your app in their paid plans.

## Troubleshooting

- If your app fails to connect to Supabase, check your network settings in Supabase to ensure it allows connections from Streamlit Cloud.
- If you encounter "Missing data" errors, ensure you've run the export_data.py script and included the data directory in your repository.
- For additional help, refer to the Streamlit documentation: https://docs.streamlit.io/streamlit-cloud

# NBA Analytics Dashboard - Streamlit App

This Streamlit application provides an interactive interface for the NBA Analytics Dashboard. It allows users to:

1. **Search for Players and Teams**: Find detailed information about NBA players and teams, including their statistics and performance metrics.

2. **Data Visualization**: Explore team performance data through interactive visualizations:
   - Points per game vs season
   - Points allowed per game vs season
   - Wins vs season
   - Home wins vs season
   - Away wins vs season

## Running the App

1. Make sure you have all dependencies installed:
   ```
   pip install -r requirements.txt
   ```

2. Activate your virtual environment:
   ```
   source venv/bin/activate
   ```

3. Run the Streamlit app:
   ```
   python streamlit_app/run.py
   ```
   
   Alternatively, you can run directly with Streamlit:
   ```
   streamlit run streamlit_app/app.py
   ```

## Features

- **Home Page**: Welcome page with an overview of the dashboard's features.
- **Search Page**: Search for players and teams with detailed statistics.
- **Data Visualization Page**: Interactive visualizations of team performance metrics across seasons.

## Data Sources

The app uses Django models to fetch data from the PostgreSQL database, which is then transformed into pandas DataFrames for analysis and visualization. 