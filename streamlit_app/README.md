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