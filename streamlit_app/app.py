import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define paths
DATA_DIR = Path(__file__).parent / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Directly load processed dataframes from CSV files
def load_csv_dataframe(filename):
    """Load a dataframe from a CSV file in the processed data directory"""
    filepath = PROCESSED_DATA_DIR / filename
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Loaded {filename} with {len(df)} records")
            return df
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
    else:
        logger.warning(f"File not found: {filepath}")
    return pd.DataFrame()

# Load all required dataframes directly from CSV files
cleaned_players_df = load_csv_dataframe("players.csv")
cleaned_teams_df = load_csv_dataframe("teams.csv")
prepared_games_df = load_csv_dataframe("games.csv")
team_metrics_df = load_csv_dataframe("team_metrics.csv")
team_rankings_df = load_csv_dataframe("team_rankings.csv")

# App setup
st.set_page_config(
    page_title="NBA Analytics Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to get seasons
def get_seasons():
    if not prepared_games_df.empty:
        return sorted(prepared_games_df['season'].unique().tolist(), reverse=True)
    return []

# Sidebar navigation
st.sidebar.title("NBA Analytics Dashboard")
pages = ["Home", "Search", "Data Visualization"]
choice = st.sidebar.radio("Navigation", pages)

# Home page
if choice == "Home":
    st.title("Welcome to the NBA Analytics Dashboard")
    st.markdown("""
    This dashboard provides insights and visualizations of NBA data. You can:
    
    - Search for specific players or teams
    - View team statistics and performance metrics
    - Explore data visualizations of team performance across seasons
    
    Use the sidebar to navigate between pages.
    """)
    
    # Display data summary
    st.subheader("Data Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Teams", len(cleaned_teams_df) if not cleaned_teams_df.empty else 0)
    
    with col2:
        st.metric("Players", len(cleaned_players_df) if not cleaned_players_df.empty else 0)
    
    with col3:
        st.metric("Games", len(prepared_games_df) if not prepared_games_df.empty else 0)
    
    # Display a welcome image
    st.image("https://cdn.nba.com/manage/2021/08/NBA-75th-anniversary-diamond-logo.jpg", width=600)

# Search page
elif choice == "Search":
    st.title("Player & Team Search")
        
    # Get list of seasons
    seasons = get_seasons()
    
    # Search tabs
    tab1, tab2 = st.tabs(["Player Search", "Team Search"])
    
    # Player Search Tab
    with tab1:
        st.subheader("Player Search")
        
        # Player search inputs
        player_name = st.text_input("Enter player name")
        selected_season = st.selectbox("Select Season", seasons if seasons else ["No data available"])
        
        if st.button("Search Player"):
            if player_name and not cleaned_players_df.empty:
                # Check if we have the full_name column
                name_col = 'full_name' if 'full_name' in cleaned_players_df.columns else 'first_name'
                
                # Filter players by name
                if 'full_name' in cleaned_players_df.columns:
                    filtered_players = cleaned_players_df[
                        cleaned_players_df['full_name'].str.contains(player_name, case=False)
                    ]
                else:
                    # Try to filter by first or last name
                    filtered_players = cleaned_players_df[
                        cleaned_players_df['first_name'].str.contains(player_name, case=False) |
                        cleaned_players_df['last_name'].str.contains(player_name, case=False)
                    ]
                    # Add full name for display
                    filtered_players['full_name'] = filtered_players['first_name'] + ' ' + filtered_players['last_name']
                
                if not filtered_players.empty:
                    # Display player cards (up to 5)
                    for _, player in filtered_players.head(5).iterrows():
                        col1, col2 = st.columns([1, 3])
                        
                        with col1:
                            # Display a placeholder NBA logo or player image if available
                            st.image("https://cdn.nba.com/logos/nba/nba-logoman-75.svg", width=100)
                        
                        with col2:
                            st.subheader(player['full_name'])
                            st.write(f"**Position:** {player['position'] if pd.notna(player['position']) else 'N/A'}")
                            st.write(f"**Height:** {player['height_feet']}-{player['height_inches'] if pd.notna(player['height_feet']) else 'N/A'}")
                            
                            # Use position_standard if available (from cleaned data)
                            if 'position_standard' in player and pd.notna(player['position_standard']):
                                st.write(f"**Standard Position:** {player['position_standard']}")
                            
                            # Team info - check for both raw and cleaned column names
                            team_name_col = next((col for col in ['team_name', 'team__full_name'] if col in player and pd.notna(player[col])), None)
                            if team_name_col:
                                st.write(f"**Team:** {player[team_name_col]}")
                            
                            team_conf_col = next((col for col in ['team_conference', 'team__conference'] if col in player and pd.notna(player[col])), None)
                            if team_conf_col:
                                st.write(f"**Team Conference:** {player[team_conf_col]}")
                            
                            team_div_col = next((col for col in ['team_division', 'team__division'] if col in player and pd.notna(player[col])), None)
                            if team_div_col:
                                st.write(f"**Team Division:** {player[team_div_col]}")
                else:
                    st.warning(f"No players found matching '{player_name}'")
    
    # Team Search Tab
    with tab2:
        st.subheader("Team Search")
        
        # Team search inputs
        if not cleaned_teams_df.empty:
            team_list = sorted(cleaned_teams_df['full_name'].unique().tolist())
            selected_team = st.selectbox("Select Team", team_list)
            selected_season = st.selectbox("Select Season", seasons if seasons else ["No data available"], key="team_season")
            
            if st.button("Search Team"):
                if selected_team and selected_season != "No data available":
                    team_id = cleaned_teams_df[cleaned_teams_df['full_name'] == selected_team]['team_id'].iloc[0]
                    
                    # Try to get team metrics from processed data first (more accurate)
                    filtered_metrics = team_metrics_df[
                        (team_metrics_df['team_id'] == team_id) & 
                        (team_metrics_df['season'] == int(selected_season))
                    ] if not team_metrics_df.empty else pd.DataFrame()
                    
                    if not filtered_metrics.empty:
                        # Display team card with advanced metrics
                        col1, col2 = st.columns([1, 3])
                        
                        with col1:
                            # Display team logo (placeholder)
                            st.image("https://cdn.nba.com/logos/nba/nba-logoman-75.svg", width=150)
                        
                        with col2:
                            # Team metrics contains more accurate and comprehensive stats
                            team_metrics = filtered_metrics.iloc[0]
                            
                            st.subheader(f"{selected_team} ({selected_season})")
                            st.write(f"**Record:** {int(team_metrics['wins'])}-{int(team_metrics['losses'])}")
                            st.write(f"**Win %:** {team_metrics['win_pct']:.3f}")
                            st.write(f"**Points Per Game:** {team_metrics['points_per_game']:.1f}")
                            st.write(f"**Points Allowed Per Game:** {team_metrics['points_allowed_per_game']:.1f}")
                            st.write(f"**Home Record:** {int(team_metrics['home_wins'])}-{int(team_metrics['home_games']-team_metrics['home_wins'])}")
                            st.write(f"**Away Record:** {int(team_metrics['away_wins'])}-{int(team_metrics['away_games']-team_metrics['away_wins'])}")
                            
                            # Show advanced metrics if available
                            if 'net_rating' in team_metrics:
                                st.write(f"**Net Rating:** {team_metrics['net_rating']:.1f}")
                            if 'offensive_rating' in team_metrics:
                                st.write(f"**Offensive Rating:** {team_metrics['offensive_rating']:.1f}")
                            if 'defensive_rating' in team_metrics:
                                st.write(f"**Defensive Rating:** {team_metrics['defensive_rating']:.1f}")
                    else:
                        # Fallback to calculating from raw game data
                        st.warning(f"No team metrics available for {selected_team} in {selected_season} season. Using raw game data instead.")
                        
                        # Calculate team stats for the selected season
                        home_games = prepared_games_df[(prepared_games_df['home_team_id'] == team_id) & (prepared_games_df['season'] == int(selected_season))]
                        away_games = prepared_games_df[(prepared_games_df['visitor_team_id'] == team_id) & (prepared_games_df['season'] == int(selected_season))]
                        
                        if not home_games.empty or not away_games.empty:
                            # Calculate wins and losses
                            home_wins = len(home_games[home_games['home_team_score'] > home_games['visitor_team_score']])
                            home_losses = len(home_games) - home_wins
                            
                            away_wins = len(away_games[away_games['visitor_team_score'] > away_games['home_team_score']])
                            away_losses = len(away_games) - away_wins
                            
                            total_wins = home_wins + away_wins
                            total_losses = home_losses + away_losses
                            
                            # Calculate points per game and points allowed
                            home_points_scored = home_games['home_team_score'].mean() if len(home_games) > 0 else 0
                            home_points_allowed = home_games['visitor_team_score'].mean() if len(home_games) > 0 else 0
                            
                            away_points_scored = away_games['visitor_team_score'].mean() if len(away_games) > 0 else 0
                            away_points_allowed = away_games['home_team_score'].mean() if len(away_games) > 0 else 0
                            
                            games_played = len(home_games) + len(away_games)
                            ppg = (home_games['home_team_score'].sum() + away_games['visitor_team_score'].sum()) / games_played if games_played > 0 else 0
                            papg = (home_games['visitor_team_score'].sum() + away_games['home_team_score'].sum()) / games_played if games_played > 0 else 0
                            
                            # Display team card
                            col1, col2 = st.columns([1, 3])
                            
                            with col1:
                                # Display team logo (placeholder)
                                st.image("https://cdn.nba.com/logos/nba/nba-logoman-75.svg", width=150)
                            
                            with col2:
                                st.subheader(f"{selected_team} ({selected_season})")
                                st.write(f"**Record:** {total_wins}-{total_losses}")
                                st.write(f"**Points Per Game:** {ppg:.1f}")
                                st.write(f"**Points Allowed Per Game:** {papg:.1f}")
                                st.write(f"**Home Record:** {home_wins}-{home_losses}")
                                st.write(f"**Away Record:** {away_wins}-{away_losses}")
                        else:
                            st.warning(f"No game data available for {selected_team} in the {selected_season} season")
        else:
            st.warning("No team data available")

# Data Visualization page
elif choice == "Data Visualization":
    st.title("Team Data Visualization")
    
    if not team_metrics_df.empty and not cleaned_teams_df.empty:
        # Team selection
        team_list = sorted(cleaned_teams_df['full_name'].unique().tolist())
        selected_team = st.selectbox("Select Team", team_list)
        
        if selected_team:
            team_id = cleaned_teams_df[cleaned_teams_df['full_name'] == selected_team]['team_id'].iloc[0]
            
            # Filter metrics for this team
            team_data = team_metrics_df[team_metrics_df['team_id'] == team_id]
            
            if not team_data.empty:
                # Get all seasons for this team
                all_seasons = sorted(team_data['season'].unique().tolist())
                
                if all_seasons:
                    # Visualization type selection
                    viz_type = st.selectbox(
                        "Select Visualization", 
                        ["Points Per Game vs Season", 
                         "Points Allowed Per Game vs Season", 
                         "Win Percentage vs Season",
                         "Home Win Percentage vs Season",
                         "Away Win Percentage vs Season",
                         "Net Rating vs Season"]
                    )
                    
                    # Create visualization based on selection
                    fig, ax = plt.subplots(figsize=(10, 6))
                    
                    if viz_type == "Points Per Game vs Season":
                        ax.bar(team_data['season'].astype(str), team_data['points_per_game'], color='blue')
                        ax.set_ylabel('Points Per Game')
                        ax.set_title(f'{selected_team} - Points Per Game by Season')
                    
                    elif viz_type == "Points Allowed Per Game vs Season":
                        ax.bar(team_data['season'].astype(str), team_data['points_allowed_per_game'], color='red')
                        ax.set_ylabel('Points Allowed Per Game')
                        ax.set_title(f'{selected_team} - Points Allowed Per Game by Season')
                    
                    elif viz_type == "Win Percentage vs Season":
                        ax.bar(team_data['season'].astype(str), team_data['win_pct'], color='green')
                        ax.set_ylabel('Win Percentage')
                        ax.set_title(f'{selected_team} - Win Percentage by Season')
                    
                    elif viz_type == "Home Win Percentage vs Season":
                        if 'home_win_pct' in team_data.columns:
                            ax.bar(team_data['season'].astype(str), team_data['home_win_pct'], color='purple')
                            ax.set_ylabel('Home Win Percentage')
                            ax.set_title(f'{selected_team} - Home Win Percentage by Season')
                        else:
                            st.warning("Home win percentage data not available")
                    
                    elif viz_type == "Away Win Percentage vs Season":
                        if 'away_win_pct' in team_data.columns:
                            ax.bar(team_data['season'].astype(str), team_data['away_win_pct'], color='orange')
                            ax.set_ylabel('Away Win Percentage')
                            ax.set_title(f'{selected_team} - Away Win Percentage by Season')
                        else:
                            st.warning("Away win percentage data not available")
                    
                    elif viz_type == "Net Rating vs Season":
                        if 'net_rating' in team_data.columns:
                            ax.bar(team_data['season'].astype(str), team_data['net_rating'], color='teal')
                            ax.set_ylabel('Net Rating')
                            ax.set_title(f'{selected_team} - Net Rating by Season')
                        else:
                            st.warning("Net rating data not available")
                    
                    ax.set_xlabel('Season')
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    
                    # Display the plot
                    st.pyplot(fig)
                    
                    # Display the data table
                    st.subheader("Data Table")
                    
                    # Select relevant columns for display
                    display_cols = ['season', 'games_played', 'wins', 'losses', 'win_pct', 
                                    'points_per_game', 'points_allowed_per_game']
                    
                    # Add advanced metrics if available
                    if 'net_rating' in team_data.columns:
                        display_cols.extend(['offensive_rating', 'defensive_rating', 'net_rating'])
                    
                    # Display the data
                    st.dataframe(team_data[display_cols].sort_values('season', ascending=False))
                    
                    # Show team rankings if available
                    if not team_rankings_df.empty:
                        st.subheader("Team Rankings")
                        team_ranking_data = team_rankings_df[team_rankings_df['team_id'] == team_id]
                        if not team_ranking_data.empty:
                            # Select ranking columns
                            ranking_cols = [col for col in team_ranking_data.columns if 'rank' in col]
                            ranking_data = team_ranking_data[['season'] + ranking_cols].sort_values('season', ascending=False)
                            st.dataframe(ranking_data)
            else:
                st.warning(f"No performance metrics available for {selected_team}")
    else:
        st.warning("No team metrics data available") 