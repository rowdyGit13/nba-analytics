# NBA Analytics Dashboard

An interactive web application for exploring NBA statistics and visualizations built with Streamlit, Django, and PostgreSQL.

## Features

- **Player Search**: Find detailed player statistics and biographical information
- **Team Analysis**: View team performance metrics and season records
- **Data Visualization**: Interactive charts displaying team performance trends
- **Responsive Design**: Mobile-friendly web interface

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Django + PostgreSQL
- **Data**: NBA API (balldontlie.io)
- **Visualization**: Matplotlib, Altair

## Data Architecture

1. **Collection**: Django commands fetch data from NBA API
2. **Storage**: PostgreSQL with CSV fallback
3. **Presentation**: Streamlit dashboard with interactive visualizations

## Quick Start

1. **Setup environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure database**:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials

   # migrate data
   python3 manage.py makemigrations nba_data
   python manage.py migrate
   ```

3. **Import data**:
   ```bash
   python manage.py import_teams
   python manage.py import_players
   python manage.py import_games # (add --seasons for specificity)
   ```

4. **Run application**:
   ```bash
   python streamlit_app/run.py
   ```

## Project Structure

- `/nba_data/`: Django models and data management
- `/streamlit_app/`: Streamlit dashboard
- `/streamlit_app/data/`: CSV fallback data

## License

MIT License 