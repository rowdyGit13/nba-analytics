# NBA Analytics Dashboard

A full-stack web application for NBA data analysis and visualization. This project demonstrates modern web development techniques and data analytics.

## Features

- Import NBA teams, players, and games data from external API
- Process and analyze NBA statistics
- Interactive data visualizations
- Responsive web interface built with Streamlit
- Persistent data storage with Supabase PostgreSQL
- Multi-tiered data architecture for reliability

## Data Flow Architecture

This project uses a three-tier data architecture:

1. **Data Import** (Weekly)
   - API data is fetched using Django management commands
   - Data is stored in local database
   - Commands: `import_teams.py`, `import_players.py`, `import_games.py`

2. **Data Migration** (Weekly)
   - Local data is migrated to Supabase cloud database
   - CSV files are generated as fallback
   - Tools: `migrate_to_supabase.py`, `supabase_manager.py`

3. **Data Consumption** (On-demand)
   - Streamlit app fetches data from Supabase when loaded
   - If cloud database is unavailable, falls back to local CSV files
   - Data is processed for analytics: `process_data.py`

## Setup and Installation

### Prerequisites

- Python 3.9+
- PostgreSQL
- Supabase account

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd nba-analytics-dashboard
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Copy the example environment file and configure your settings:
   ```bash
   cp .env.example .env
   # Edit .env with your database and API credentials
   ```

4. Initialize the database:
   ```bash
   python manage.py migrate
   ```

5. Import initial data:
   ```bash
   python manage.py import_teams
   python manage.py import_players
   python manage.py import_games --seasons 2023
   ```

6. Migrate data to Supabase:
   ```bash
   python supabase_manager.py --migrate
   ```

7. Run the application:
   ```bash
   python streamlit_app/run.py
   ```

## Automated Data Updates

The project includes a weekly update script that automates the data pipeline:

```bash
python weekly_update.py
```

This script:
- Imports latest NBA data
- Migrates data to Supabase
- Processes analytics

You can customize the update process with flags:
```bash
python weekly_update.py --no-import  # Skip importing new data
python weekly_update.py --no-migrate  # Skip Supabase migration
python weekly_update.py --no-process  # Skip data processing
```

## Project Structure

- `/nba_data/` - Django app for data models and management commands
- `/nba_data/management/commands/` - Data import commands
- `/nba_data/analytics/` - Data processing modules
- `/streamlit_app/` - Streamlit frontend application
- `/streamlit_app/data/` - CSV fallback data files
- `supabase_manager.py` - Tool for managing Supabase data
- `weekly_update.py` - Automated data pipeline script

## Deployment

This application can be deployed in multiple ways:

1. **Local Development**:
   ```bash
   python streamlit_app/run.py
   ```

2. **Streamlit Cloud**:
   - Connect your GitHub repository to Streamlit Cloud
   - Point to `streamlit_app/app.py` as the main file
   - Add your environment variables in the Streamlit Cloud dashboard

3. **Self-Hosted**:
   - Deploy Django and Streamlit components separately
   - Set up weekly data updates with cron or Task Scheduler

## License

[MIT License](LICENSE)

## Acknowledgements

- [NBA API](https://www.balldontlie.io) for providing basketball data
- [Streamlit](https://streamlit.io) for the frontend framework
- [Supabase](https://supabase.io) for database hosting 