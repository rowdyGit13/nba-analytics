# NBA Analytics Dashboard (Streamlit App)

This is a Streamlit frontend for the NBA Analytics project. It can run in two modes:
1. **Integrated Mode** - Connected to the Django backend
2. **Standalone Mode** - Using pre-exported CSV data files

## Standalone Mode Setup

To run the app in standalone mode (without Django):

1. Make sure you have Python 3.8+ installed
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the setup script to prepare data directories:
   ```
   python setup_standalone.py
   ```
4. Launch the Streamlit app:
   ```
   streamlit run app.py
   ```

## Data Files

The app requires the following CSV files in the `data/processed/` directory:
- `players.csv` - NBA player data
- `teams.csv` - NBA team data
- `games.csv` - Game results data
- `team_metrics.csv` - Calculated team performance metrics
- `team_rankings.csv` - Team rankings based on performance

## Deploying to Streamlit Cloud

To deploy to Streamlit Cloud:

1. Make sure all required CSV files are in the `data/processed/` directory
2. Push the repository to GitHub
3. Connect Streamlit Cloud to your GitHub repository
4. Set the main file path to `streamlit_app/app.py`
5. Use the requirements file at `streamlit_app/requirements.txt`

## Troubleshooting

If you encounter the "Failed to load necessary modules" error:

1. Check that all required CSV files exist in the `data/processed/` directory
2. Verify that all dependencies are installed
3. Run the setup script: `python setup_standalone.py`
4. Check the Streamlit logs for detailed error messages

## Features

- Team and player search functionality
- Team performance visualization
- Statistical analysis of NBA data
- Responsive design for desktop and mobile viewing 