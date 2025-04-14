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

2. **Activate venv and migrate your data to Supabase**:
   ```bash
   # Activate virtual environment
   source venv/bin/activate
   
   # Run the setup script
   python3 manage.py makemigrations nba_data
   python3 manage.py migrate
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

## Data Loading Process

The application uses a two-step approach for data loading:

1. **Primary Method**: Direct loading from Django models/database
   - The `data_loader` module directly accesses Django models to fetch and process data
   - This approach provides the most up-to-date information

2. **Fallback Method**: CSV files
   - If direct loading fails, the application falls back to pre-processed CSV files
   - CSV files are automatically generated when running `run.py`

## How to Run

1. Make sure your virtual environment is activated:
   ```
   source venv/bin/activate
   ```

2. Run the application:
   ```
   cd streamlit_app
   python3 run.py
   ```

This will:
1. Set up the Django environment
2. Generate backup CSV files
3. Start the Streamlit server

## File Structure

- `run.py`: Main entry point for the application
- `app.py`: The Streamlit dashboard interface
- `data_loader/`: Module for loading data from Django models or CSV files
  - `load_data.py`: Contains functions to load data from both sources
- `data/processed/`: Directory containing backup CSV files

## Troubleshooting

If you encounter issues with direct data loading:
1. Check your Django database connection
2. Ensure the required models (Teams, Players, Games) have data
3. Run the process_data command manually to generate CSV files:
   ```
   python3 manage.py process_data --export --export-dir streamlit_app/data/processed
   ```

## Features

- **Home Page**: Welcome page with an overview of the dashboard's features.
- **Search Page**: Search for players and teams with detailed statistics.
- **Data Visualization Page**: Interactive visualizations of team performance metrics across seasons.

## Data Sources

The app uses Django models to fetch data from the PostgreSQL database, which is then transformed into pandas DataFrames for analysis and visualization.

# NBA Analytics Dashboard - Chart Utilities

This module provides tools for creating standardized, team-branded visualizations for NBA data analysis.

## Features

- Team color integration with all visualizations
- Styled tables with conditional formatting
- Team-colored bar charts and line charts
- Shot charts with basketball court overlay
- Player comparison radar charts
- Bubble charts for multi-dimensional analysis

## Usage

### Demo Application

To see all chart utilities in action, run the demo application:

```bash
streamlit run streamlit_app/demo.py
```

### Styling DataFrames

```python
import pandas as pd
from streamlit_app.chart_utils import style_dataframe

# Create or load your DataFrame
df = pd.DataFrame({
    "Player": ["Player A", "Player B"],
    "PPG": [25.3, 20.6],
    "FG_PCT": [0.48, 0.52]
})

# Apply team styling
styled_df = style_dataframe(df, "Lakers")

# Display in Streamlit
st.dataframe(styled_df)
```

### Creating Team-Colored Charts

```python
import pandas as pd
from streamlit_app.chart_utils import create_team_bar_chart, create_team_line_chart

# Create your DataFrame
df = pd.DataFrame({
    "Season": ["2021-22", "2022-23"],
    "PPG": [110.5, 115.2]
})

# Create bar chart
bar_chart = create_team_bar_chart(
    df=df,
    x_col="Season",
    y_col="PPG",
    team_name="Celtics",
    title="Celtics Points Per Game"
)

# Display in Streamlit
st.altair_chart(bar_chart, use_container_width=True)
```

### Shot Charts

```python
import pandas as pd
from streamlit_app.chart_utils import create_shot_chart

# Load your shot data with LOC_X, LOC_Y, SHOT_MADE_FLAG columns
shots_df = pd.DataFrame({
    "LOC_X": [-100, 150, 220],
    "LOC_Y": [50, 200, 150],
    "SHOT_MADE_FLAG": [1, 0, 1]
})

# Create shot chart
shot_chart = create_shot_chart(
    shots_df=shots_df,
    team_name="Warriors",
    made_only=False,
    title="Warriors Shot Chart" 
)

# Display in Streamlit
st.pyplot(shot_chart)
```

### Player Comparison

```python
from streamlit_app.chart_utils import create_player_comparison_radar

# Define player stats
player1_stats = {
    "PTS": 25.3, "REB": 5.7, "AST": 7.9,
    "STL": 1.5, "BLK": 0.6, "FG%": 0.48, "3P%": 0.38
}

player2_stats = {
    "PTS": 20.6, "REB": 10.1, "AST": 3.2,
    "STL": 0.9, "BLK": 1.7, "FG%": 0.52, "3P%": 0.33
}

# Create comparison radar chart
radar_chart = create_player_comparison_radar(
    player1_stats=player1_stats,
    player2_stats=player2_stats,
    player1_name="LeBron James",
    player2_name="Nikola Jokić"
)

# Display in Streamlit
st.pyplot(radar_chart)
```

### Bubble Charts

```python
import pandas as pd
from streamlit_app.chart_utils import create_bubble_chart

# Create a DataFrame with team data
teams_df = pd.DataFrame({
    "Team": ["Lakers", "Celtics", "Warriors"],
    "PPG": [115.2, 118.3, 120.1],
    "OPP_PPG": [110.5, 108.7, 114.3],
    "WIN_PCT": [0.65, 0.70, 0.62]
})

# Create bubble chart
bubble_chart = create_bubble_chart(
    df=teams_df,
    x_col="PPG",
    y_col="OPP_PPG",
    size_col="WIN_PCT",
    team_col="Team",
    title="Offensive vs Defensive Performance"
)

# Display in Streamlit
st.altair_chart(bubble_chart, use_container_width=True)
```

## Available Functions

- `style_dataframe(df, team_name)`: Style a DataFrame with team colors
- `create_team_bar_chart(df, x_col, y_col, team_name, title)`: Create a bar chart with team colors
- `create_team_line_chart(df, x_col, y_col, team_name, title)`: Create a line chart with team colors
- `create_shot_chart(shots_df, team_name, made_only, title)`: Create a shot chart on a basketball court
- `create_player_comparison_radar(player1_stats, player2_stats, player1_name, player2_name)`: Create a radar chart comparing two players
- `create_bubble_chart(df, x_col, y_col, size_col, team_col, title)`: Create a bubble chart with team colors 